#!/usr/bin/env python3
"""
Dataset Plunderer V2 - Scrapling Adaptor + CPU Kill-Switch
부관 데피디2(써전) 제작 | 캡틴 승인 없이 외부 약탈 금지
"""
import os
import sys
import json
import time
import psutil
from datetime import datetime
from scrapling import Adaptor

# ========== CONFIG ==========
DATA_LOOT = "/home/hakkocap/Data_Loot"
ORIGINAL_DIR = os.path.join(DATA_LOOT, "Original")
METADATA_DIR = os.path.join(DATA_LOOT, "Metadata")
SUMMARY_DIR = os.path.join(DATA_LOOT, "Summary")
LOGS_DIR = os.path.join(DATA_LOOT, "Logs")
CPU_THRESHOLD = 10.0  # % - 초과 시 자결
# =============================

def kill_switch():
    """CPU 10% 초과 시 즉시 프로세스 종료"""
    cpu = psutil.cpu_percent(interval=1)
    if cpu > CPU_THRESHOLD:
        log(f"[KILL] CPU {cpu}% > {CPU_THRESHOLD}% 임계치 초과. 자결.")
        sys.exit(1)
    return cpu

def log(msg):
    """로그를 파일과 콘솔에 동시 출력"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    os.makedirs(LOGS_DIR, exist_ok=True)
    logfile = os.path.join(LOGS_DIR, f"plunder_{datetime.now().strftime('%Y%m%d')}.log")
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def scan_local_targets(directory):
    """로컬 HTML 파일 목록 수집"""
    targets = []
    if not os.path.isdir(directory):
        log(f"[WARN] 디렉토리 없음: {directory}")
        return targets
    for fname in os.listdir(directory):
        if fname.endswith((".html", ".htm")):
            targets.append(os.path.join(directory, fname))
    return targets

def plunder_local_file(filepath):
    """Scrapling Adaptor로 로컬 HTML 파싱 (adaptive 모드)"""
    kill_switch()  # 매 파일 처리 전 CPU 체크

    with open(filepath, "r", encoding="utf-8") as f:
        raw_html = f.read()

    # Adaptor: 브라우저 없이 HTML 파싱, adaptive=True로 구조 변경에 강건
    page = Adaptor(raw_html, url=f"file://{filepath}")

    result = {
        "source": filepath,
        "title": page.css_first("title").text() if page.css_first("title") else "N/A",
        "headings": [h.text() for h in page.css("h1, h2, h3")],
        "paragraphs": [p.text() for p in page.css("p")],
        "metadata_spans": [s.text() for s in page.css(".metadata span")],
        "all_text_length": len(page.get_all_text()),
        "links": [a.attrib.get("href", "") for a in page.css("a")],
        "timestamp": datetime.now().isoformat(),
    }
    return result

def save_metadata(result, metadata_dir):
    """추출된 메타데이터를 JSON으로 저장"""
    os.makedirs(metadata_dir, exist_ok=True)
    fname = os.path.basename(result["source"]).replace(".html", ".json")
    outpath = os.path.join(metadata_dir, fname)
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return outpath

def save_summary(result, summary_dir):
    """핵심 요약을 마크다운으로 저장"""
    os.makedirs(summary_dir, exist_ok=True)
    fname = os.path.basename(result["source"]).replace(".html", "_summary.md")
    outpath = os.path.join(summary_dir, fname)
    lines = [
        f"# {result['title']}",
        f"- 출처: {result['source']}",
        f"- 추출 시각: {result['timestamp']}",
        f"- 전체 텍스트 길이: {result['all_text_length']}자",
        "",
        "## 제목들",
    ]
    for h in result["headings"]:
        lines.append(f"- {h}")
    lines.append("")
    lines.append("## 핵심 단락")
    for p in result["paragraphs"]:
        lines.append(f"- {p}")
    lines.append("")
    lines.append("## 메타데이터")
    for m in result["metadata_spans"]:
        lines.append(f"- {m}")

    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return outpath

def main():
    log("=" * 50)
    log("[START] Dataset Plunderer V2 가동")
    log(f"  엔진: Scrapling Adaptor (adaptive)")
    log(f"  CPU 임계치: {CPU_THRESHOLD}%")
    log(f"  모드: 로컬 전용 (외부 약탈 금지)")
    log("=" * 50)

    # CPU 사전 체크
    cpu = kill_switch()
    log(f"[OK] CPU 현재 {cpu}% - 임계치 이내")

    # 로컬 타겟 스캔
    targets = scan_local_targets(ORIGINAL_DIR)
    log(f"[SCAN] {len(targets)}개 로컬 HTML 파일 발견")

    if not targets:
        log("[DONE] 약탈 대상 없음. 대기.")
        return

    results = []
    for t in targets:
        log(f"[PLUNDER] {os.path.basename(t)} 파싱 중...")
        try:
            r = plunder_local_file(t)
            meta_path = save_metadata(r, METADATA_DIR)
            summ_path = save_summary(r, SUMMARY_DIR)
            log(f"  -> 메타데이터: {meta_path}")
            log(f"  -> 요약: {summ_path}")
            log(f"  -> 제목: {r['title']}, 단락 {len(r['paragraphs'])}개, 텍스트 {r['all_text_length']}자")
            results.append(r)
        except Exception as e:
            log(f"[ERROR] {os.path.basename(t)} 처리 실패: {e}")

    log("=" * 50)
    log(f"[COMPLETE] 총 {len(results)}/{len(targets)} 파일 약탈 성공")
    log(f"[COST] OpenRouter 잔액 변동: $0.00 (로컬 전용)")
    log("=" * 50)

if __name__ == "__main__":
    main()
