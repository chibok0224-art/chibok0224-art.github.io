# GigCompass 할 일

## 제휴 승인 후
- [ ] `content/site.json` 의 `affiliate.bta` 에 제휴 ID 넣기
- [ ] 대시보드에서 만든 딥링크 하나와 비교해 `landing_page_encode_times`(1 또는 2) 맞추기
- [ ] 제휴 약관에서 긱 이미지 사용 규칙 확인 → 허용되면 `show_gig_images` 를 true 로
- [ ] 가이드 6개에 추천 판매자 채우기 (스킬: "○○ 추천 판매자 채워줘")

## 가이드
- [ ] [CONTENT_PLAN.md](CONTENT_PLAN.md) 순서대로 2~3개씩 작성 (1~4순위 40개 모두 완료, 가이드 총 47개. 다음 목록은 새로 정해야 함)
- [x] 겹치는 서비스 연결 (2026-09-25, build.py `link_showcase_copies`): AI Services·Consulting 페이지의 같은 서비스(예: AI Development)도 원래 대분류의 가이드로 연결되게
- [ ] 도메인과 Search Console 연결 1~2개월 뒤, 실제 검색어를 보고 CONTENT_PLAN.md 순서 다시 매기기

## 도메인을 산 뒤 (순서대로)
1. [ ] **도메인 연결** (Claude): GitHub Pages 에 Custom domain 연결, DNS 안내, `base_url` 변경 → 사이트맵과 canonical 이 새 도메인으로 바뀜. 기존 github.io 주소는 자동으로 넘어감
2. [ ] **Google Search Console** (직접 로그인): 반드시 1번 **뒤에**. 소유 확인 코드는 Claude 가 넣고, `sitemap.xml` 제출
3. [ ] **Bing Webmaster Tools** (직접 로그인): Search Console 에서 가져오기. Bing, DuckDuckGo, Yahoo, AI 검색에 노출
4. [ ] **네이버 서치어드바이저** (직접 로그인): 효과는 적지만 무료
