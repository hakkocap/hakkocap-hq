// 캡틴스 대시보드 React UI 컴포넌트 템플릿
import React, { useState, useEffect } from 'react';

const CaptainDashboard = ({ disciplinaryData }) => {
  const [score, setScore] = useState(1500);
  const [efficiency, setEfficiency] = useState('98%');
  const [recentActions, setRecentActions] = useState([]);

  useEffect(() => {
    if (disciplinaryData) {
      // 데이터 파싱 및 상태 설정
      const data = JSON.parse(disciplinaryData);
      setScore(data.captain_score || 1500);
      setEfficiency(data.nanobot_efficiency || '98%');
      setRecentActions(data.recent_actions || []);
    }
  }, [disciplinaryData]);

  // 점수에 따른 게이지 색상 계산
  const getGaugeColor = (score) => {
    if (score >= 1600) return '#44ff44'; // 우수
    if (score >= 1400) return '#ffaa00'; // 양호
    return '#ff4444'; // 개선 필요
  };

  return (
    <div style={styles.dashboard}>
      <h1 style={styles.title}>🏴‍☠️ 캡틴스 대시보드</h1>
      
      <div style={styles.grid}>
        {/* 상벌점 게이지 패널 */}
        <div style={styles.panel}>
          <h2 style={styles.panelTitle}>상벌점 게이지</h2>
          <div style={styles.gaugeContainer}>
            <div 
              style={{
                ...styles.gauge,
                width: `${Math.min(100, (score - 1000) / 10)}%`,
                backgroundColor: getGaugeColor(score)
              }}
            />
          </div>
          <div style={styles.scoreDisplay}>
            <span style={styles.scoreLabel}>현재 점수:</span>
            <span style={styles.scoreValue}>{score} 점</span>
          </div>
          <div style={styles.efficiency}>
            나노봇 효율: <span style={styles.efficiencyValue}>{efficiency}</span>
          </div>
        </div>

        {/* 활동 로그 패널 */}
        <div style={styles.panel}>
          <h2 style={styles.panelTitle}>활동 로그</h2>
          <table style={styles.logTable}>
            <thead>
              <tr>
                <th style={styles.th}>시간</th>
                <th style={styles.th}>크루</th>
                <th style={styles.th}>행동</th>
                <th style={styles.th}>점수</th>
              </tr>
            </thead>
            <tbody>
              {recentActions.map((action, index) => (
                <tr key={index} style={index % 2 === 0 ? styles.trEven : styles.trOdd}>
                  <td style={styles.td}>{action.time}</td>
                  <td style={styles.td}>{action.crew}</td>
                  <td style={styles.td}>{action.action}</td>
                  <td style={styles.td}>
                    <span style={action.points > 0 ? styles.positive : styles.negative}>
                      {action.points > 0 ? '+' : ''}{action.points}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 상태 표시줄 */}
      <div style={styles.statusBar}>
        <span style={styles.statusItem}>Phase 1: ✅ 완료</span>
        <span style={styles.statusItem}>Phase 2: 🚀 진행 중</span>
        <span style={styles.statusItem}>업데이트: {new Date().toLocaleTimeString()}</span>
      </div>
    </div>
  );
};

// 인라인 스타일 (CSS 대체)
const styles = {
  dashboard: {
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#1a1a1a',
    color: '#ffffff',
    padding: '20px',
    borderRadius: '10px',
    maxWidth: '1200px',
    margin: '0 auto'
  },
  title: {
    textAlign: 'center',
    marginBottom: '30px',
    color: '#ffaa00'
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '20px',
    marginBottom: '20px'
  },
  panel: {
    backgroundColor: '#2d2d2d',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.3)'
  },
  panelTitle: {
    marginTop: '0',
    color: '#44ff44',
    borderBottom: '2px solid #444',
    paddingBottom: '10px'
  },
  gaugeContainer: {
    height: '30px',
    backgroundColor: '#444',
    borderRadius: '15px',
    overflow: 'hidden',
    margin: '20px 0'
  },
  gauge: {
    height: '100%',
    transition: 'width 0.5s ease'
  },
  scoreDisplay: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '10px'
  },
  scoreLabel: {
    fontSize: '18px'
  },
  scoreValue: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#ffaa00'
  },
  efficiency: {
    textAlign: 'center',
    fontSize: '16px',
    color: '#aaa'
  },
  efficiencyValue: {
    color: '#44ff44',
    fontWeight: 'bold'
  },
  logTable: {
    width: '100%',
    borderCollapse: 'collapse'
  },
  th: {
    padding: '12px',
    textAlign: 'left',
    borderBottom: '2px solid #444',
    color: '#ffaa00'
  },
  td: {
    padding: '10px',
    borderBottom: '1px solid #444'
  },
  trEven: {
    backgroundColor: '#333'
  },
  trOdd: {
    backgroundColor: '#2d2d2d'
  },
  positive: {
    color: '#44ff44',
    fontWeight: 'bold'
  },
  negative: {
    color: '#ff4444',
    fontWeight: 'bold'
  },
  statusBar: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '10px',
    backgroundColor: '#2d2d2d',
    borderRadius: '5px',
    fontSize: '14px'
  },
  statusItem: {
    color: '#aaa'
  }
};

export default CaptainDashboard;
