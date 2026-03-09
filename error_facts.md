# 오류 팩트 보고 (08:49)

## 1. Langflow 커스텀 컴포넌트 등록 실패
### 문제
- 예상 경로: `/home/hakkocap/.openclaw/workspace/langflow_dir/.venv/lib/python3.13/site-packages/langflow/components/custom`
- 실제 상태: 디렉토리 존재하지 않음
- 영향: 오프니의 dashboard_db_node.py 컴포넌트 등록 불가

### 원인 분석
1. Langflow 설치 버전 차이 (커스텀 컴포넌트 구조 변경 가능성)
2. uv 가상환경 특이성 (표준 경로와 다를 수 있음)
3. 문서화 부족 (공식 등록 방법 불명확)

## 2. 데이터베이스 접근 문제
### 문제
- 예상 DB: `/home/hakkocap/다운로드/swp/data/test.db`
- 실제 상태: 파일 존재 여부 불명 (확인 필요)
- 영향: 실제 데이터 연동 불가, Mock 데이터만 가능

## 3. React 컴포넌트 주입 기술적 장벽
### 문제
- Langflow UI 수정 방법 불명확
- React 컴포넌트 삽입 포인트(Injection Point) 탐색 실패
- 프론트엔드 빌드 프로세스 이해 필요

## 4. 통신 및 협력 문제
### 문제
- 오프니 응답 지연: 07:47 → 08:48 (61분)
- 진행 상태 공유 부재
- 문제 발생 시 즉시 보고 체계 미구축

## 5. 시간 관리 문제
### 문제
- 예상: Phase 1 (20분) → Phase 2 (52분) = 72분
- 실제: Phase 1 (61분+) 미완료, Phase 2 미시작
- 지연: 85분+ (예상 대비 118% 초과)
