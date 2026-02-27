#!/usr/bin/env python3
"""
⚓ Sujuon Weapon Selection Routine
自动化武器偵察システム - Daily GitHub Scraping Tool Analysis
Created: 2026-02-27
Purpose: Auto scout, test, and filter best scraping tools
"""
import os
import time
import docker
import requests
from github import Github
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta

# ============== Configuration ==============
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")  # Set via env
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")
SCRAPING_TAGS = ['topic:web-scraping', 'topic:crawler', 'topic:scraping-framework', 'topic:browser-automation']

# Resource Limits (Ship Safety)
MEMORY_LIMIT = "512m"  # 512MB max
CPU_QUOTA = 50000       # 50% CPU limit
TEST_DURATION = 60       # 60 seconds max test
# ==========================================

class WeaponStrategist:
    def __init__(self):
        self.gh = Github(GITHUB_TOKEN) if GITHUB_TOKEN else None
        self.docker_client = None
        try:
            self.docker_client = docker.from_env()
        except Exception as e:
            print(f"[WARN] Docker not available: {e}")
        self.report_data = []
    
    def scout_github(self):
        """1. Daily Scouting: GitHub Trending 탐색"""
        if not self.gh:
            print("[ERROR] GitHub Token not configured")
            return []
        
        print(f"[{datetime.now()}] 🚀 Scouting started...")
        
        # Search for recent repos with scraping tags
        date cutoff = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        query = f"{' '.join(SCRAPING_TAGS)} pushed:>{cutoff}"
        
        try:
            repos = self.gh.search_repositories(
                query=query, 
                sort='stars', 
                order='desc'
            )
            return list(repos[:10])
        except Exception as e:
            print(f"[ERROR] GitHub search failed: {e}")
            return []
    
    def sandbox_test(self, repo):
        """2. Sandbox Verification: Docker 기반 모의 실험"""
        if not self.docker_client:
            return {"verdict": "Skip (No Docker)", "cpu": 0, "mem": 0}
        
        name = repo.name
        clone_url = repo.clone_url
        verdict = "Discard"
        stats = {"cpu": 0, "mem": 0}
        
        container = None
        try:
            # Create ephemeral container for testing
            container = self.docker_client.containers.run(
                "python:3.10-slim",
                command=f"sh -c 'apt-get update && apt-get install -y git && git clone {clone_url} /app && cd /app && pip install . --dry-run 2>&1'",
                detach=True,
                remove=True,
                mem_limit=MEMORY_LIMIT,
                cpu_quota=CPU_QUOTA,
                timeout=TEST_DURATION
            )
            
            # Monitor for duration
            start_time = time.time()
            max_mem = 0
            
            while time.time() - start_time < TEST_DURATION:
                try:
                    container.reload()
                    stats = container.stats(stream=False)
                    mem = stats.get('memory_stats', {}).get('usage', 0) / 1024 / 1024  # MB
                    max_mem = max(max_mem, mem)
                except:
                    break
                time.sleep(5)
            
            # Check result
            exit_code = container.wait(timeout=5).get('StatusCode', 1)
            
            if exit_code == 0 and max_mem < 450:  # Under 450MB
                verdict = "Deploy" if repo.stargazers_count > 100 else "On Hold"
            else:
                verdict = f"Discard (mem:{max_mem:.0f}MB)"
            
            stats["mem"] = max_mem
            
        except Exception as e:
            verdict = f"Discard ({str(e)[:30]})"
        finally:
            if container:
                try:
                    container.stop(timeout=5)
                except:
                    pass
        
        return {"verdict": verdict, "cpu": stats["cpu"], "mem": stats["mem"]}
    
    def generate_report(self):
        """4. Morning Report Generation"""
        if not TELEGRAM_TOKEN or not CHAT_ID:
            print("[WARN] Telegram not configured, printing to console")
            self.print_console_report()
            return
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        deploy_count = len([d for d in self.report_data if 'Deploy' in d['verdict']])
        
        header = f"⚓️ **Captain, Weapon Scout Report ({now})**\n"
        header += f"Scanned {len(self.report_data)} tools. Found {deploy_count} viable blades.\n\n"
        
        table = "| Tool | ⭐ | Verdict | Description |\n|---|---|---|---|\n"
        for data in self.report_data:
            table += f"| {data['name']} | {data['stars']} | {data['verdict']} | {data['desc'][:30]} |\n"
        
        self.send_telegram(header + table)
    
    def print_console_report(self):
        """Console fallback"""
        print("\n" + "="*60)
        print("⚓ WEAPON SCOUT REPORT")
        print("="*60)
        for data in self.report_data:
            print(f"{data['name']:30} | {data['stars']:5}⭐ | {data['verdict']}")
        print("="*60 + "\n")
    
    def send_telegram(self, message):
        """Telegram notification"""
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        try:
            requests.post(url, data={
                "chat_id": CHAT_ID, 
                "text": message, 
                "parse_mode": "Markdown"
            }, timeout=10)
            print("[OK] Telegram report sent")
        except Exception as e:
            print(f"[ERROR] Telegram failed: {e}")
    
    def daily_routine(self):
        """Main daily routine"""
        self.report_data = []
        
        # Step 1: Scout
        repos = self.scout_github()
        
        # Step 2: Test each repo
        for repo in repos:
            result = self.sandbox_test(repo)
            self.report_data.append({
                "name": repo.name,
                "stars": repo.stargazers_count,
                "verdict": result["verdict"],
                "desc": repo.description if repo.description else "No desc",
                "url": repo.html_url
            })
            time.sleep(1)  # Rate limit
        
        # Step 3: Report
        self.generate_report()

# ============== Entry Point ==============
def main():
    strategist = WeaponStrategist()
    
    # Check if first run (no schedule)
    print("⚓ Sujuon Weapon System Active")
    print(f"GitHub: {'✅' if strategist.gh else '❌'}")
    print(f"Docker: {'✅' if strategist.docker_client else '❌'}")
    print(f"Telegram: {'✅' if TELEGRAM_TOKEN else '❌'}")
    
    # Run once immediately for testing
    print("\n🚀 Running initial scan...")
    strategist.daily_routine()
    
    # Schedule daily at 09:00
    scheduler = BlockingScheduler()
    scheduler.add_job(strategist.daily_routine, 'cron', hour=9, minute=0)
    
    print("\n⏰ Scheduler active. Waiting for 09:00 daily...")
    print("Press Ctrl+C to stop.\n")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Stopped.")

if __name__ == "__main__":
    main()
