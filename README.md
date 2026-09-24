# GigCompass: Fiverr 제휴 추천 사이트

주소: https://chibok0224-art.github.io (GitHub Pages)

추가로 설치할 것이 없는 정적 사이트다. `content/` 를 고치고 `build.py` 를 돌리면 `dist/` 가 새로 만들어진다.
GitHub 에 push 하면 GitHub Actions 가 `python build.py --release` 로 빌드해서 자동으로 공개한다.

## 사이트 구조 (Fiverr 와 같은 3단)

```
대분류 (Graphics & Design)                 /graphics-design/
 └ 그룹 (Logo & Brand Identity)            대분류 페이지 안의 상자
    └ 서비스 (Logo Design)
         가이드가 있으면 → 우리 페이지       /graphics-design/logo-design/
         가이드가 없으면 → Fiverr 로 바로 (제휴 링크)
```

- 홈: 대분류 카드 + 최근 가이드
- `/services/`: 모든 서비스를 A–Z 로 한 목록에서 검색
- 서비스 페이지: 추천 판매자(상위 5개 카드 + 나머지 검색·정렬 목록), 고르는 법 가이드, FAQ, 같은 그룹의 다른 서비스

## 폴더

| 경로 | 내용 |
|---|---|
| `content/site.json` | 사이트 이름, 주소, **제휴 링크 틀**(`affiliate_link_template`) |
| `content/taxonomy/<대분류>.json` | 대분류 → 그룹 → 서비스 목록 (Fiverr 카테고리 그대로) |
| `content/pages/<대분류>/<서비스>/` | 우리가 쓴 가이드: `page.json`(제목·소개·FAQ) + `guide.html`(본문) |
| `content/gigs.csv` | 추천 판매자. 한 줄에 한 명, `page` 열로 서비스에 연결 |
| `tools/import_taxonomy.py` | Fiverr 카테고리 목록을 taxonomy 파일로 저장 |
| `static/` | CSS, 검색 스크립트, 아이콘 |
| `dist/` | 결과물. 직접 고치지 않는다 (git 에도 안 올림) |

## 명령

```
python build.py              # 미리보기용: draft 판매자도 점선 카드로 보임
python build.py --release    # 공개용: live 판매자만. 오류가 있으면 멈춤
python -m http.server 8080 --directory dist   # http://localhost:8080 에서 미리보기
```

## 제휴 링크 틀

Fiverr 어필리에이트 승인 후, 대시보드에서 아무 Fiverr 주소로 딥링크를 하나 만들어 보고
그 모양에 맞춰 `affiliate_link_template` 을 채운다. 원래 Fiverr 주소가 들어갈 자리는 `{url}` 로 쓴다.
그러면 사이트의 **모든** 카테고리 링크가 한 번에 제휴 링크가 된다. 비어 있으면 일반 Fiverr 링크다.

## gigs.csv 열

| 열 | 뜻 |
|---|---|
| `id` | 겹치지 않는 영문 이름 (예: `ugc-jane-doe`) |
| `page` | 서비스 경로 (예: `video-animation/ugc-videos`). 그 서비스에 가이드가 있어야 한다 |
| `status` | `live` 는 공개, `draft` 는 미리보기에서만 |
| `rank` | 서비스 안 순서. 작을수록 위 |
| `name`, `best_for`, `gig_title` | 판매자 이름, "Best for ..." 한 줄, 긱 제목 |
| `rating`, `reviews`, `level`, `starting_price` | 평점, 리뷰 수, 등급, 시작 가격(달러 숫자만) |
| `checked` | 위 숫자를 확인한 날짜 `YYYY-MM-DD`. 120일이 지나면 빌드가 경고한다 |
| `why`, `watch_out` | 추천 이유(우리 말로), 솔직한 단점 |
| `affiliate_url` | 그 판매자 긱의 제휴 딥링크 |

엑셀로 편집하면 저장할 때 **"CSV UTF-8"** 형식을 고른다.

## 지킬 것

- 제휴 고지는 모든 페이지 하단과 추천·대분류 페이지 상단에 자동으로 붙는다. 지우지 않는다.
- 후기를 지어내지 않고, 판매자 포트폴리오 이미지를 가져오지 않는다.
- 도메인이나 사이트 이름에 "Fiverr" 를 넣지 않는다 (상표).
- 서비스 페이지는 직접 쓴 가이드가 있을 때만 만든다. 빈 페이지 수백 개는 구글이 낮게 본다.
- Fiverr 에서 자동 수집 중 봇 확인 화면이 나오면 멈춘다. 사람 확인은 사용자가 직접 한다.
