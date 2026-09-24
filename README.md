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
| `content/site.json` | 사이트 이름, 주소, **제휴 ID**(`affiliate.bta`) |
| `content/taxonomy/<대분류>.json` | 대분류 → 그룹 → 서비스 목록 (Fiverr 카테고리 그대로) |
| `content/pages/<대분류>/<서비스>/` | 우리가 쓴 가이드: `page.json`(제목·소개·FAQ) + `guide.html`(본문) |
| `content/gigs.csv` | 추천 판매자. 한 줄에 한 명, `page` 열로 서비스에 연결 |
| `tools/import_taxonomy.py` | Fiverr 카테고리 목록을 taxonomy 파일로 저장 |
| `tools/picks.py` | 추천 판매자 순위 매기기(select), gigs.csv 에 넣기(add) |
| `tools/category_art.py` | 대분류 카드 일러스트(SVG) 생성 |
| `.claude/skills/gigcompass-picks/` | 스킬: 추천 판매자 자동 선정 ("○○ 추천 판매자 채워줘") |
| `.claude/skills/gigcompass-guide/` | 스킬: 새 가이드 작성·게시 ("가이드 써줘", CONTENT_PLAN.md 순서) |
| `.claude/skills/gigcompass-refresh/` | 스킬: 오래된 판매자 카드 점검·갱신·교체 ("사이트 점검해줘") |
| `CONTENT_PLAN.md`, `TODO.md` | 가이드 작성 순서, 할 일 목록 |
| `static/` | CSS, 검색 스크립트, 아이콘 |
| `dist/` | 결과물. 직접 고치지 않는다 (git 에도 안 올림) |

## 명령

```
python build.py              # 미리보기용: draft 판매자도 점선 카드로 보임
python build.py --release    # 공개용: live 판매자만. 오류가 있으면 멈춤
python -m http.server 8080 --directory dist   # http://localhost:8080 에서 미리보기
```

## 제휴 링크 (딥링크)

Fiverr 딥링크는 모두 같은 모양이다:
`https://go.fiverr.com/visit/?bta=<제휴 ID>&brand=<상품>&landingPage=<Fiverr 주소>`

`content/site.json` 의 `affiliate.bta` 에 대시보드의 제휴 ID 만 넣으면 사이트의 **모든** Fiverr 링크
(카테고리 420개, 추천 판매자 버튼, Logo Maker 버튼)가 자동으로 딥링크가 된다. 비어 있으면 일반 Fiverr 링크다.

- `brand` 는 자동으로 고른다: Vetted Pro 판매자 → `fp`, Logo Maker → `logomaker`, 나머지 → `fiverrmarketplace`
- `landing_page_encode_times`: 대시보드가 만든 실제 딥링크의 `landingPage` 가 `https%3A` 로 시작하면 1, `https%253A` 면 2

가이드 본문(guide.html)에서는 `{{fiverr:/주소|버튼 문구}}` 라고 쓰면 딥링크 버튼이 된다.

## 추천 판매자 자동 선정 (스킬)

Claude Code 에서 "Logo Design 추천 판매자 채워줘" 처럼 말하면 `.claude/skills/gigcompass-picks` 가 돈다.

1. Fiverr 목록 페이지를 읽는다
2. `tools/picks.py select` 가 **Vetted Pro 판매자(평점 4.7·리뷰 20개 이상)를 먼저** 뽑고, 자리가 남을 때만
   일반 판매자(평점 4.8·리뷰 100개 이상)로 채운다. Pro 가 모자라면 목록 2페이지까지 먼저 본다
3. 상위 긱 페이지를 읽고 카드 문구를 우리 말로 쓴다
4. `tools/picks.py add` 가 gigs.csv 에 넣는다 → 빌드·게시

Fiverr 봇 확인("It needs a human touch")이 뜨면 멈추고 사용자에게 풀어 달라고 한다.

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
| `gig_url` | 판매자 긱의 **일반** Fiverr 주소. 빌드가 딥링크로 바꾼다 |
| `affiliate_url` | (선택) 직접 만든 딥링크. 있으면 gig_url 대신 쓴다 |
| `gig_image` | 긱 대표(광고) 이미지 주소(`https://fiverr-res.cloudinary.com/...`). 스킬이 판매자를 고를 때 자동으로 모은다. 카드 위 배너로 나오지만, **`site.json` 의 `show_gig_images` 가 true 일 때만** 보인다 (제휴 약관 확인 전까지 false) |
| `photo` | (선택) 판매자가 사용을 허락한 사진. `static/img/sellers/` 에 두고 `/img/sellers/파일명` 으로 적는다. 없으면 이니셜 아바타 |

엑셀로 편집하면 저장할 때 **"CSV UTF-8"** 형식을 고른다.

## 지킬 것

- 제휴 고지는 모든 페이지 하단과 추천·대분류 페이지 상단에 자동으로 붙는다. 지우지 않는다.
- 후기를 지어내지 않고, 판매자 포트폴리오 이미지를 가져오지 않는다.
- 도메인이나 사이트 이름에 "Fiverr" 를 넣지 않는다 (상표).
- 서비스 페이지는 직접 쓴 가이드가 있을 때만 만든다. 빈 페이지 수백 개는 구글이 낮게 본다.
- Fiverr 에서 자동 수집 중 봇 확인 화면이 나오면 멈춘다. 사람 확인은 사용자가 직접 한다.
