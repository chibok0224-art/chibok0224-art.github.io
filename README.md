# GigCompass: Fiverr 제휴 추천 사이트

주소: https://chibok0224-art.github.io (GitHub Pages)

추가로 설치할 것이 없는 정적 사이트다. `content/` 를 고치고 `build.py` 를 돌리면 `dist/` 가 새로 만들어진다.
GitHub 에 push 하면 GitHub Actions 가 `python build.py --release` 로 빌드해서 자동으로 공개한다.

## 폴더

| 경로 | 내용 |
|---|---|
| `content/site.json` | 사이트 이름, 주소(base_url), 연락 이메일 |
| `content/gigs.csv` | **모든 긱을 한 줄씩** 적는 표. 수백 개가 되어도 이 파일 하나 |
| `content/categories/<분야>/category.json` | 분야 제목, 그룹(Marketing 등), 큰 카드 개수, FAQ |
| `content/categories/<분야>/guide.html` | 분야별 고르는 법 가이드 본문 |
| `static/` | CSS, 아이콘 (그대로 복사됨) |
| `build.py` | 사이트 생성 스크립트 |
| `.github/workflows/deploy.yml` | push 하면 자동 빌드·공개 |
| `dist/` | 결과물. 직접 고치지 않는다 (git 에도 안 올림) |

## 명령

```
python build.py              # 미리보기용: draft 긱도 점선 카드로 보임
python build.py --release    # 공개용: live 긱만. live 줄에 오류가 있으면 멈춤
python -m http.server 8080 --directory dist   # http://localhost:8080 에서 미리보기
```

## gigs.csv 열

| 열 | 뜻 |
|---|---|
| `id` | 겹치지 않는 영문 이름 (예: `ugc-jane-doe`). 페이지 안 링크에 쓰임 |
| `category` | 분야 폴더 이름 (예: `ugc-video-creators`) |
| `status` | `live` 는 공개, `draft` 는 미리보기에서만 |
| `rank` | 분야 안 순서. 작을수록 위. 상위 `featured_count` 개(기본 5)는 큰 카드, 나머지는 검색·정렬되는 목록 |
| `name`, `best_for`, `gig_title` | 판매자 이름, "Best for ..." 한 줄, 긱 제목 |
| `rating`, `reviews`, `level`, `starting_price` | 평점, 리뷰 수, 등급, 시작 가격(달러 숫자만) |
| `checked` | 위 숫자를 확인한 날짜 `YYYY-MM-DD`. 120일이 지나면 빌드가 경고한다 |
| `why`, `watch_out` | 추천 이유(우리 말로), 솔직한 단점 |
| `affiliate_url` | Fiverr 어필리에이트 대시보드에서 만든 딥링크 |

엑셀로 편집하면 저장할 때 **"CSV UTF-8"** 형식을 고른다. 그냥 "CSV" 로 저장하면 글자가 깨질 수 있다.

## 새 분야 추가

`content/categories/ugc-video-creators/` 폴더를 복사해 이름을 바꾸고, `category.json` 과 `guide.html` 을 새 분야에 맞게 쓴다.
홈 화면에는 `group` 별로 묶여 나온다.

## 지킬 것

- 제휴 고지는 모든 페이지 하단과 추천 페이지 상단에 자동으로 붙는다. 지우지 않는다.
- 후기를 지어내지 않고, 판매자 포트폴리오 이미지를 가져오지 않는다.
- 평점·가격은 확인한 날짜와 함께 사실대로 적는다.
- 도메인이나 사이트 이름에 "Fiverr" 를 넣지 않는다 (상표).
- 긱이 수백 개라도 분야마다 가이드는 직접 쓴 좋은 글이어야 한다. 링크만 나열한 페이지는 구글이 낮게 본다.
