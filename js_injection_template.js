// 캡틴스 대시보드 JS Injection 템플릿
// React 렌더링 후 DOM에 강제 삽입

(function() {
    'use strict';
    
    // 대시보드 UI HTML
    const dashboardHTML = `
        <div id="captain-dashboard-js" style="
            position: fixed;
            top: 10px;
            right: 10px;
            width: 350px;
            background: #1e1e2f;
            color: white;
            border: 2px solid #4caf50;
            border-radius: 8px;
            z-index: 999999;
            padding: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            font-family: sans-serif;
        ">
            <h3 style="margin: 0 0 10px 0; color: #4caf50;">🏴‍☠️ Captain's Board (JS)</h3>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span>Score:</span> <strong style="font-size: 1.2em; color: #fff;">1500</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>Swarm Eff:</span> <strong style="font-size: 1.2em; color: #03a9f4;">98%</strong>
            </div>
            <div style="margin-top: 10px; font-size: 0.8em; color: #aaa;">
                JS Injection v1.0
            </div>
        </div>
    `;
    
    // 대시보드 삽입 함수
    function injectDashboard() {
        // 기존 대시보드 제거 (중복 방지)
        const existingDashboard = document.getElementById('captain-dashboard-js');
        if (existingDashboard) {
            existingDashboard.remove();
        }
        
        // 새 대시보드 생성 및 삽입
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = dashboardHTML;
        const dashboard = tempDiv.firstElementChild;
        
        // body에 직접 추가 (React root보다 위에)
        document.body.appendChild(dashboard);
        
        console.log('✅ 캡틴스 대시보드 JS Injection 완료');
        return dashboard;
    }
    
    // MutationObserver로 DOM 변경 감지
    function waitForReactRender() {
        return new Promise((resolve) => {
            // React root div 찾기 (일반적인 React 앱 구조)
            const reactRoot = document.getElementById('root') || 
                             document.querySelector('[data-reactroot]') ||
                             document.querySelector('body > div:first-child');
            
            if (reactRoot && reactRoot.children.length > 0) {
                console.log('✅ React root 발견, 렌더링 완료로 판단');
                resolve(true);
                return;
            }
            
            // MutationObserver로 DOM 변경 감지
            const observer = new MutationObserver((mutations) => {
                for (const mutation of mutations) {
                    if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                        // React-like 요소 발견 시
                        const hasReactContent = document.querySelector('#root, [data-reactroot], .App, .react-root');
                        if (hasReactContent) {
                            observer.disconnect();
                            console.log('✅ DOM 변경 감지, React 렌더링 완료');
                            resolve(true);
                            return;
                        }
                    }
                }
            });
            
            // body 감시 시작
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
            
            // 타임아웃 (10초 후 강제 실행)
            setTimeout(() => {
                observer.disconnect();
                console.log('⚠️ 타임아웃, 강제 삽입 시도');
                resolve(true);
            }, 10000);
        });
    }
    
    // 지속적 존재 확인 (React가 다시 덮어쓸 경우 대비)
    function ensureDashboardPresence() {
        setInterval(() => {
            const dashboard = document.getElementById('captain-dashboard-js');
            if (!dashboard) {
                console.log('⚠️ 대시보드 사라짐, 재삽입');
                injectDashboard();
            }
        }, 3000); // 3초마다 확인
    }
    
    // 메인 실행
    console.log('🚀 캡틴스 대시보드 JS Injection 시작');
    
    // DOM 로딩 완료 대기
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            waitForReactRender().then(() => {
                injectDashboard();
                ensureDashboardPresence();
            });
        });
    } else {
        waitForReactRender().then(() => {
            injectDashboard();
            ensureDashboardPresence();
        });
    }
    
    // 전역 함수로 노출 (디버깅용)
    window.__captainDashboard = {
        inject: injectDashboard,
        remove: () => {
            const dashboard = document.getElementById('captain-dashboard-js');
            if (dashboard) dashboard.remove();
        },
        version: '1.0'
    };
    
})();
