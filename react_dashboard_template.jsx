// Langflow 대시보드 주입용 React 컴포넌트 템플릿 (오프니 초안)
import React, { useState, useEffect } from 'react';

const CaptainDashboard = () => {
  const [data, setData] = useState({ captain_score: 0, nanobot_efficiency: "0%", recent_actions: [] });

  useEffect(() => {
    // Phase 1에서 뚫어놓은 Langflow API 엔드포인트 호출
    const fetchData = async () => {
      try {
        const response = await fetch('/api/v1/run/dashboard_flow');
        const result = await response.json();
        // 실제 데이터 파싱 구조는 Langflow 출력 형태에 맞게 수정
        setData(result.data_json); 
      } catch (error) {
        console.error("대시보드 데이터 수신 실패", error);
      }
    };
    fetchData();
    // 30초마다 자동 갱신
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '20px', backgroundColor: '#1e1e2f', color: '#fff', borderRadius: '8px' }}>
      <h2>🏴‍☠️ 캡틴스 대시보드 (Langflow UI Edition)</h2>
      <div style={{ display: 'flex', gap: '20px', marginTop: '15px' }}>
        <div style={{ flex: 1, padding: '15px', background: '#2d2d44', borderRadius: '5px' }}>
          <h3>현재 상벌점 스코어</h3>
          <p style={{ fontSize: '2em', fontWeight: 'bold', color: '#4caf50' }}>{data.captain_score} 점</p>
        </div>
        <div style={{ flex: 1, padding: '15px', background: '#2d2d44', borderRadius: '5px' }}>
          <h3>나노봇 스웜 효율</h3>
          <p style={{ fontSize: '2em', fontWeight: 'bold', color: '#03a9f4' }}>{data.nanobot_efficiency}</p>
        </div>
      </div>
      <div style={{ marginTop: '20px' }}>
        <h3>최근 활동 (Recent Actions)</h3>
        <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #555' }}>
              <th>액션</th>
              <th>스코어 변동</th>
            </tr>
          </thead>
          <tbody>
            {data.recent_actions.map((act, idx) => (
              <tr key={idx}>
                <td>{act.action}</td>
                <td style={{ color: act.score.startsWith('+') ? '#4caf50' : '#f44336' }}>{act.score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CaptainDashboard;
