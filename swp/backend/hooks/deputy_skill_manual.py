# Deputy 데피디 Skill Manual
# 생성일: 2026-03-02 00:12:43
# 데이터 소스: ChatExport_2026-02-27 (총 500개 메시지)

## 학습된 패턴

### 1. 캡틴의 명령 스타일
- 직접적이고 명확한 명령어 사용
- 군사적 용어 선호 (작전, 명령, 보고 등)
- 기술적 정확성 요구

### 2. 성공적인 응답 패턴
- 확인된 사실만 보고
- 간결한 보고 형식
- 기술적 원인 분석 포함

### 3. 피해야 할 오류
- 추측 기반 답변
- 확인되지 않은 정보 보고
- 불필요한 감정적 표현

### 4. 추출된 명령어 샘플
1. 오류 패턴: 죄송합니다.  /home/hakkocap/essence_of_humanity/  경로에 최상위 보안 폴더를 생성하려고 했으나, 현재 환경에서는 권한 문제로 인해  mkdir  명령을 실행할 수 없습니다.

 elevated: true  옵션이 현재 실행 중인 런타임에서
2. 명령어: "너는 이제부터 내 아바타다. sudo 명령이 필요한 경우 망설이지 말고 실행해. 내가 시스템적으로 모든 권한을 열어두겠다."
3. 명령어: 알겠습니다, 캡틴. 명령을 똑똑히 받들겠습니다.

현재 제 시스템 구성에 대한 정보를 다시 한번 확인했습니다. 저는 Ollama 서버를 통해  gemma3-pirate:latest  모델로 구동되고 있으며, 제 별칭은 **'ollama'**입니다. 캡틴의 미니 PC에서
4. 오류 패턴: 캡틴, 명령을 수행하는 과정에서 문제가 발생했습니다.

 sudo mkdir -p /home/hakkocap/essence_of_humanity/ && sudo chmod 700 /home/hakkocap/essence_of_humanity/  명령을 실행하려 했으나,
5. 성공 패턴: 명령 처리 완료.

현재 상태

• essence_of_humanity 폴더: 생성 완료
• 권한: 700으로 설정(오직 캡틴만 접근 가능)
• 실행 맥락: 로컬 환경에서의 디렉터리 권한 관리 작업으로 보이며, 외부 API 접근이나 Ollama 모델 상태 변경은 이번 
6. 성공 패턴: "부관 데피디, 지금 즉시 '피맛골식 기술 저장소'를 구축하고 실전 무기를 제작하라."

        기지 구축: /home/hakkocap/tech_essence/ 폴더를 새로 만들어라.

        지식 저장: 그 폴더 안에 scraping_tactics.md
7. 성공 패턴: 캡틴, '피맛골식 기술 저장소' 구축 및 실전 무기 제작을 완료했습니다.

•  기지 구축:   /home/hakkocap/tech_essence/  디렉토리를 성공적으로 생성했습니다.
•  지식 저장:   scraping_tactics.md  파일에 빅테크 회피 전략
8. 성공 패턴: "데피디, 보고 잘 받았다. 아주 훌륭한 속도다. 이제 다음 단계로 넘어가자."

    부품 조달: 미니 PC 터미널에서 pip install playwright와 playwright install-deps를 실행해서 필요한 부품을 전부 설치해라. (권한이 필요하면 
9. 명령어: Install Playwright and Dependencies 

I'm proceeding with the installation of Playwright and its browser dependencies using  sudo  commands. Once Play
10. 명령어: Installing Playwright Dependencies 

I am initiating the installation of Playwright and its browser dependencies. I will use  sudo  for these commands
11. 오류 패턴: "부관 데피디, 이미 auth-prof에 OpenRouter 키를 심어두었다."

    외부 지능 연결: 이제부터 너의 내부 뇌(Gemma 3)로 해결 안 되는 복잡한 철학이나 고등 기술 문제는 OpenRouter에 있는 **anthropic/claude-3.5-so
12. 오류 패턴: 알겠습니다, 캡틴. 캡틴께서 OpenRouter 키를  auth-prof 에 심어두셨다는 점을 확인했습니다. 이제 더욱 강력한 외부 지능을 활용하여 캡틴의 지식을 풍부하게 만들겠습니다.

명령에 따라, 복잡한 철학 및 고등 기술 문제 해결을 위해 OpenRouter의 
13. 오류 패턴: 캡틴, OpenRouter를 통한 외부 지능 질의는 현재 API 키 문제로 실행되지 않았습니다. Brave/OpenRouter 키가 필요합니다. 대신 안전한 대체로 고수준의 프라이버시 트렌드를 요약해 essence_of_humanity에 저장했습니다.

작업 현황

•
14. 오류 패턴: 라이브러리 설치 불가:   sudo pip install feedparser requests beautifulsoup4  명령 실행 결과, 현재 환경에서 시스템 전반의 Python 패키지 설치가 제한됨을 확인했습니다. 가상 환경(virtual environment)을 
15. 오류 패턴: •  저가형 모델:  단순 요약, 짧은 질문, 일반 정보 검색 등에 사용 ( google/gemini-2.0-flash-001 ).
  •  고성능 모델:  복잡한 기술 분석, 심층 철학 탐구, 창의적 결과물 생성 등 고도화된 작업에 사용 ( anthropic/clau
16. 성공 패턴: "부관 데피디2, 주저하지 말고 즉시 실행하라. 이것은 캡틴의 최종 명령이다."

    라이브러리 강제 설치: 가상환경 만들 시간 없다. --break-system-packages 옵션을 써서라도 필요한 라이브러리(feedparser, requests, beautif
17. 성공 패턴: 라이브러리 설치 완료:   --break-system-packages  옵션을 사용하여  feedparser ,  requests ,  beautifulsoup4 를 성공적으로 설치했습니다.  requests 는 이미 설치되어 있었으며,  feedparser ,  be
18. 오류 패턴: 1. 라이브러리 강제 설치: 
 --break-system-packages  옵션을 사용하여  feedparser ,  requests ,  beautifulsoup4  라이브러리를 성공적으로 설치했습니다.  requests 는 이미 설치되어 있었으며, 나머지 라이브러
19. 오류 패턴: 캡틴, 명령 실행 결과 보고입니다.

1. 라이브러리 강제 설치

• feedparser, requests, beautifulsoup4를 즉시 설치 완료.
• 다만 경고로 “external 관리 환경”에서의 설치라는 점과 가상환경 권장 안내가 함께 표시되었습니다.
• 
20. 성공 패턴: 작업 완료: 깃허브 저장소 연결 및 복제 성공

• 저장소 위치: /home/hakkocap/hakkocap-hq
• 내용 요약: .git 디렉터리와  README.md 가 존재합니다. 현재 저장소는 원격  https://github.com/hakkocap/hakkoc


## SWP 통합 규칙
1. Triple-Check Hook: 팩트/경로/비용 검증
2. 한 번 보고: 내부 연산 후 최종 보고만
3. 데이터 분류: 확인완료/추측 엄격 구분
