# 에이전트 문서 규약 v1

이 문서는 네 저장소가 같은 자리에서 문서 종류·원본·검사자를 알아보기 위한 규격이다.
통일이 목표가 아니다. 숫자는 이 채팅에서 명령으로 다시 센 값이며, 확인하지 못한
경로는 비워 둔다.

확인 범위(2026-08-30):

| 저장소 | 확인 방법 | HEAD / 브랜치 |
| --- | --- | --- |
| `the-via-eerraa` | `git clone --depth 1` 후 `ls`/`wc`/`rg` | 기본 브랜치 `main` |
| `eerraa-qmk-h7s-fw` | 같음 | 기본 브랜치 `main` |
| `qmk_firmware_eerraa` | `--branch cursor/era-docs-commit-d-c7b9` (커밋 D 이후) | `e8f6b580` |
| `eerraa-54lm20-fw` | `gh api repos/eerraa/eerraa-54lm20-fw` → **404** | 확인 못 함 |

계획 §1.5의 자매 수치(앱 1,996줄, H7S 1,110줄, 54lm20 13편/`docs/_archive/`)는
이번 채팅에서 그대로 재현되지 않거나 저장소에 닿지 못했으므로 옮기지 않는다.

---

## 1. 목적과 독자

네 저장소(`the-via-eerraa`, `qmk_firmware_eerraa`, `eerraa-qmk-h7s-fw`,
`eerraa-54lm20-fw`) 사이를 오가는 에이전트가 다음을 **같은 자리**에서 찾는다.

- 이건 어떤 종류의 문서인가
- 무엇의 원본인가
- 어긋나면 무엇이 잡아 주는가

목표는 네 트리를 한 형식으로 합치는 것이 아니라, 형식이 달라도 **알아볼 수 있음**이다.
`AGENTS.md`는 저장소마다 달라도 된다. 헤더 두 줄, 장르 다섯, 거절 세 줄, 최소 검사
네 종은 같다.

---

## 2. 문서 헤더

문서 집합이 있는 디렉터리 아래 모든 에이전트 문서는 첫머리에 두 줄만 선언한다.

```
Genre: contract
Canonical for: 이 문서가 유일한 원본인 사실
```

- **`Genre:`** — 담아도 되는 문장 종류. 값은 §3의 다섯 중 하나.
- **`Canonical for:`** — 비면 안 된다. 빈 선언은 없는 것보다 나쁘다.
- **`Status:`** — 값이 실제로 변하는 ADR에서만. 허용 값은 `Proposed` / `Accepted` /
  `Superseded`. 그 밖 문서는 유효하거나 삭제되거나 둘 중 하나라 상수가 된다.
- **`Read when:`** — 쓰지 않는다. 언제 읽는가는 진입 색인이 소유한다.

저장소 루트의 `AGENTS.md`·`CLAUDE.md`는 진입 사슬이지 색인이 라우팅하는 문서가
아니므로 헤더를 갖지 않는다.

이번 채팅에서 확인한 헤더:

| 저장소 | `Genre` + `Canonical for` | `Status:` | `Read when:` |
| --- | --- | --- | --- |
| `qmk_firmware_eerraa` (커밋 D 이후, 에이전트 문서 21편) | 21/21 | 0건 (`rg '^(Status\|Read when):'` 무) | 0건 |
| `the-via-eerraa` `docs/*.md` 7편 | 7/7 | 번호 있는 ADR 3편만 `Accepted` (`docs/adr/README.md`에는 없음) | 0건. `tests/docs-contract.test.ts`가 부재를 검사 |
| `eerraa-qmk-h7s-fw` `docs/*.md` 6편 | 6/6 | 0건 | 0건 |
| `eerraa-54lm20-fw` | 확인 못 함 | 확인 못 함 | 확인 못 함 |

QMK 쪽에서 `Status:`를 뺀 근거(계획 §6·커밋 D): 21편 중 20편이 `active`, 변종 1.
`Read when:`은 색인 행과 같은 사실의 중복이었다. 이 규격은 그 결정을 공통으로 둔다.

---

## 3. 장르 5종과 문장 종류

장르가 문장 종류를 결정한다. 다섯뿐이고 늘리지 않는다.

| 장르 | 담는 문장 |
| --- | --- |
| `contract` | 무엇이 참이어야 하는가. 규칙·불변식·거절. 설계가 바뀌기 전까지 선다. |
| `map` | 어디에 무엇이 있는가. 이름·경로·소유. 코드가 옮기기 전까지 선다. |
| `manual` | 어떻게 돌리는가. 절차·명령·판정. 계기가 바뀌기 전까지 선다. |
| `state` | 무엇이 남았는가. 빚·보류·캠페인 중의 측정. 캠페인이 끝나면 지운다. |
| `entry` | 진입 체인. 읽기 정책과 라우터. |

문장이 장르에 맞지 않으면 그 문서는 틀린 것이다. 기계가 장르-문장 정합을 무는지는
저장소마다 다르다 — 이번 채팅에서 확인한 검사기는 헤더 **값**이 다섯 중 하나인지만
본다.

QMK `AGENTS.md`(커밋 D 이후)는 state 문서가 지금 없다고 적는다. 장르 자체는 남겨 둔다.
H7S는 `docs/state_open.md`가 `Genre: state`다.

---

## 4. 디렉터리

에이전트 문서가 **약 20편을 넘으면** 장르별 디렉터리(`contracts/` `maps/` `manuals/`
등). 그 이하면 **flat**이고 장르는 헤더가 선언한다.

이번 채팅에서 확인한 배치:

| 저장소 | 에이전트 `.md` | 배치 |
| --- | --- | --- |
| `qmk_firmware_eerraa` | 21 (`find keyboards/era/common/docs -name '*.md' \| wc -l`) | `contracts/` 10 · `maps/` 3 · `manuals/` 7 · 그 위 `era_active_index.md`. `docs/user/`는 사용자 안내 3파일(`.txt`)이며 검사기가 헤더 대상에서 뺀다 |
| `the-via-eerraa` | 7 (`docs/` 3 + `docs/adr/` 4) | flat + ADR 하위. 장르 디렉터리 없음 |
| `eerraa-qmk-h7s-fw` | 6 (모두 `docs/` 바로 아래) | flat. `docs/readme.txt`는 사용자 안내이며 색인이 「에이전트 문서 규격의 예외」로 적음. `docs/_archive/` 없음 |
| `eerraa-54lm20-fw` | 확인 못 함 | 확인 못 함 |

QMK 21편은 임계를 넘으므로 장르 디렉터리는 이 절과 맞다. 계획은 그래도 이를
선언된 이탈로 적는다(§14).

---

## 5. 진입 라우터

두 층이다.

1. **`AGENTS.md`** — 정체, 작업 규칙, 읽기 정책, 함정 절. 루트에 둔다.
2. **색인** — 모든 에이전트 문서가 여기서 도달 가능해야 한다. 작업 행은 세 열:
   **Change**(편집 전 필독) / **Locate**(조회) / **Verify**(빌드·캡처·판정 시).

세 열을 한 목록으로 합치지 않는다. 읽기 이유는 서로 다르다.

이번 채팅에서 확인한 라우터:

| 저장소 | `AGENTS.md` | 색인 | Change / Locate / Verify |
| --- | --- | --- | --- |
| `qmk_firmware_eerraa` | 루트. `## Startup Read Policy`, `## Navigation` | `keyboards/era/common/docs/era_active_index.md` (`Genre: entry`). 표 머리 `Task area \| Change — read first \| Locate \| Verify` | 있음 |
| `the-via-eerraa` | 루트. §1이 할 일→문서 표 | `docs/MAP.md` (`Genre: map`) | 세 열 표는 없음. 할 일 표는 한 열 |
| `eerraa-qmk-h7s-fw` | 루트. §1이 할 일→문서 표 | `docs/MAP.md` §2 (`Genre: map`). 표 머리 `문서 \| Genre \| 무엇의 원본인가` | 세 열 표는 없음 |
| `eerraa-54lm20-fw` | 확인 못 함 | 확인 못 함 | 확인 못 함 |

---

## 6. 단일 사실 소유

같은 사실을 두 문서에 쓰지 않는다. 한 곳에 두고 가리킨다.

- 각 문서의 `Canonical for:`가 그 문서의 범위다. 새 사실을 쓰기 전에 이미 원본을
  선언한 문서가 있는지 본다.
- 함수가 무엇을 하는지 말하는 문단은 그 함수가 사는 파일을 댄다.
- 검사기가 소스에서 다시 계산할 수 있는 수는 검사기가 정본이다. 손으로 고치는
  표는 그 나머지만 든다.

확인한 예: 앱 `docs/MAP.md` §1은 「이 문서는 파생물」이고 숫자를
`tests/docs-contract.test.ts`가 매니페스트에서 다시 계산한다. H7S `docs/MAP.md`의
보드·채널 표는 `<!-- era-doc-refs: … -->` 마커가 있고
`python tools/era_doc_refs.py --tables`가 소스를 다시 계산한다고 문서가 적는다.

---

## 7. 거절 블록

결정이 내려진 자리 옆에 세 줄. 따로 모은 목록을 만들지 않는다.

```
> **REFUSED:** 거절한 것
> **WHY:** 거절하는 결과. 한 문장으로 홀로 서야 한다
> **REOPENS:** 다시 열 증거 또는 조건. 영구면 그렇게 적는다
```

세 줄이 이미 최소다. 장황하다는 이유로 줄이지 않는다.

확인: QMK `AGENTS.md` `### A refusal is three lines…`가 위 형식을 고정한다.
H7S `docs/contract_usb.md`가 같은 세 줄을 쓴다. 앱 `the-via-eerraa`의 `*.md`에서는
이번 채팅의 `rg`가 `REFUSED`/`WHY`를 찾지 못했다.

---

## 8. 은퇴

- 대체된 사실은 교체한다. 옛것과 나란히 두지 않는다.
- 닫힌 계획은 삭제한다. 「닫힘」표시로 남기지 않는다.
- **아카이브 트리를 만들지 않는다.** 색인되는 평행 트리는 현재로 오인된다.
- 삭제 커밋은 지운 내용이 들고 있던 판단을 본문에 보존한다. 삭제는 이 환경에서
  되돌릴 히스토리가 없는 저장소가 있으므로 복구 불가능한 수다.
- 삭제 전 안전망: 지운 줄이 들고 있던 식별자가 이제 집이 없으면(homeless)
  승격 후보다. 삭제가 아니다.

확인: QMK `AGENTS.md` **Evidence And Retirement**가 위와 같다. 검사기의
`--homeless`는 `keyboards/era/common/tools/era_doc_refs.py` docstring에 있다.
H7S `docs/`에 `_archive/` 없음(`ls`). 54lm20의 `_archive/`는 이번 채팅에서
확인하지 못했다.

---

## 9. 검사 카탈로그

검사가 볼 수 있는 종류의 목록이다. 구현은 저장소마다 고른다.

| 종류 | 무는 것 |
| --- | --- |
| path | 백틱/링크 경로가 트리에 있는가 |
| citation | `path:line`(또는 구간)이 파일 안인가 |
| section | 가리킨 절 제목이 있는가 |
| header | `Genre:`·`Canonical for:` 존재, 장르 값, 은퇴 필드 부재 |
| index | 색인이 가리키는 파일이 있고, 모든 에이전트 문서가 색인에서 도달하는가 |
| claims | 함수가 무엇을 한다는 문단이 파일을 대는가 |
| source comments | 소스 주석이 부르는 문서 경로가 있는가 |
| constants | 문서의 상수 값이 트리 값과 같은가 |
| homeless | 삭제한 줄의 식별자가 이제 집이 없는가 |
| symbol | 백틱 식별자가 소스/도구에 있는가 |
| table | 생성 표가 소스 재계산과 같은가 |
| menu | 펌웨어가 라우팅하는 메뉴가 정의 JSON에서 도달하는가 |
| version | 문서의 버전 리터럴이 현재를 넘지 않는가 |
| number provenance | 문서의 숫자가 소스에서 다시 나오는가 |

**최소 필수 4종: path · header · index · citation.**

저장소별 구현 위치 — **이번 채팅에서 `ls`/`wc`로 확인한 것만**:

| 저장소 | 경로 | 줄 | 이번 채팅에서 읽은 검사 |
| --- | --- | --- | --- |
| `qmk_firmware_eerraa` | `keyboards/era/common/tools/era_doc_refs.py` | 768 | 파일 머리 설정 블록. docstring 기본 8종: paths · citations · sections · headers · index · claims · source comments · constant values. 요청 시 `--homeless`. `HEADERS = ("Genre:", "Canonical for:")`, `FORBIDDEN_HEADERS = ("Status:", "Read when:")`, `FOREIGN_REPOS = ("the-via-eerraa/", "eerraa-qmk-h7s-fw/", "eerraa-54lm20-fw/", "eerraa-agent-docs/")` |
| `eerraa-qmk-h7s-fw` | `tools/era_doc_refs.py` | 507 | docstring 9종: path · comment · header · index · symbol · retired · table · menu · version. `FOREIGN_REPOS = ("the-via-eerraa/", "qmk_firmware_eerraa/", "eerraa-qmk-h7s-boot/", "eerraa-54lm20-fw/")`. citation을 별도 항목으로 적지는 않음. 경로 정규식은 `:line`을 받는다 |
| `the-via-eerraa` | `tests/docs-contract.test.ts` | 512 | `names only real repository paths` · `citations point at a line that exists` · `declares Genre and Canonical for`(ADR만 `Status`, `Read when` 부재) · `every document is reachable from the entry chain`. 매니페스트·wire 상수 재계산 |
| `eerraa-54lm20-fw` | 확인 못 함 | — | — |

검사기 이식: 공유 패키지 없음. QMK 검사기 머리의
`# --- repository-specific, and the only part another repository has to change ---`
블록과 `FOREIGN_REPOS` 접두사(`resolve()`가 `skip`)를 복사한다. 타 저장소 경로는
저장소 이름을 앞에 붙인다.

---

## 10. 실행 경로

커밋마다 자동으로 검사하는 것이 권장이다.

- **권장:** 버전관리된 `hooks/pre-commit` + 클론당 `git config core.hooksPath hooks`.
  호스트(에이전트·터미널)와 무관하다.
- 패키지 스크립트나 CI가 있으면 거기에 넣는다.
- **일반 셸·읽기·검색 호출에 훅을 걸지 않는다.**

확인한 실행 경로:

| 저장소 | 자동 | 수동 | CI |
| --- | --- | --- | --- |
| `qmk_firmware_eerraa` | `hooks/pre-commit`(index 모드 `100755`)이 `hooks/era_commit_check.py`를 부름. 주석: 클론당 `git config core.hooksPath hooks`. `--no-verify` 금지 | 검사기 직접 실행 | 이 채팅에서 워크플로를 열지 않음 |
| `the-via-eerraa` | 패키지 스크립트 `bun run test:p1`이 `tests/docs-contract.test.ts`를 포함 (`package.json`) | 같음 | `.github/workflows/pr-build.yml`은 `bun run build`만. `test:p1`/`docs-contract` 문자열 없음. `AGENTS.md`도 「PR CI는 `bun run build` 하나만」이라고 적음 |
| `eerraa-qmk-h7s-fw` | `hooks/` 디렉터리 없음. `git config core.hooksPath` 미설정 | `python tools/era_doc_refs.py` (`AGENTS.md` §5) | 이 채팅에서 워크플로를 열지 않음 |
| `eerraa-54lm20-fw` | 확인 못 함 | 확인 못 함 | 확인 못 함 |

---

## 11. 함정 절

제목은 둘 중 하나다.

- 한국어: **먼저 알아야 손해를 안 보는 것**
- 영어: **What Costs Time If You Do Not Know It**

조사로 알기 어렵고, 모르면 시간을 잃는 것만 적는다. 각 항목은 규칙이 **사는 곳**을
가리키는 포인터다. 함정 절 자체가 정본이 아니다.

확인: 앱 `AGENTS.md` §2, H7S `AGENTS.md` §2가 한국어 제목을 쓴다. QMK는 커밋 D
시점에 이 절이 없고, 계획 §7.2가 커밋 E에서 영어 제목으로 넣을 예정이다(이 규격
저장소의 일이 아니다).

---

## 12. 금지

다음을 탐색 층으로 **의무화하지 않는다.**

- 의무형 지식 그래프
- 검색 전 훅
- 세션마다 생성하는 컨텍스트

근거는 QMK 커밋 C 본문(`41fd891c`)과 계획 §5.4다. 제품명은 트리에 두지 않는다.
측정치는 그 커밋 본문에만 있다.

커밋 C 본문에서 확인한 수치:

- 자연어 architecture 질의 2회가 231/745 노드로 퍼짐
- CLI ≈0.7 s vs `rg` 0.106 s
- 로컬 3,986파일 424 MiB (그 클론은 tracked만 9.4M, 스냅샷 없음)
- tracked 9.5 MB
- 앱 저장소 75,000줄 오커밋
- 모든 Bash 호출에 붙은 어댑터 비용

계획 §5.4의 `AGENTS.md` `## Navigation` REFUSED 블록(커밋 D 브랜치에서 확인):
라우터와 검색이 같은 질문에 답하는 동안 위 비용을 남겼다. REOPENS는 호출 비용이
셸 검색보다 낮고, 답을 에이전트 읽기 이외의 것이 검사하는 도구다.

앱 `AGENTS.md` §2와 `docs/MAP.md` §8도 펌웨어 cwd로 연 세션이 앱에
`graphify-out/` 75,000줄을 오커밋한 사고를 적는다.

현행 H7S는 이 절과 충돌한다. `AGENTS.md` §3이 `graphify-out/`·
`python tools/graphify/bootstrap.py`·세션 시작 훅을 구조 질의의 경로로 두고,
클론에 `graphify-out/`·`.graphifyignore`·`tools/graphify/`가 있다. v1을 채택하면
이 의무를 거두거나 §14에 이탈로 선언해야 한다. 지금은 채택 문구가 없다.

---

## 13. 저장소 간 짝 항목

교차 저장소 검사는 이번 채팅에서 확인한 구현이 없다. **짝 자체가 검사다.**
표 형식: 사실 · 이쪽 위치 · 저쪽 위치 · 어긋나면 잡는 것.

양쪽 경로를 이 채팅에서 `ls`로 본 것만:

| 사실 | 이쪽 | 저쪽 | 어긋나면 잡는 것 |
| --- | --- | --- | --- |
| 어느 보드에 어느 VIA 메뉴가 있는가 | `qmk_firmware_eerraa` `keyboards/era/**/keymaps/via/*-VIA.json` — `git ls-files` **26**개 | `the-via-eerraa/tests/era-definition.test.ts`의 `FEATURE_COVERAGE` (`rg`로 심볼 확인) | 없음. 앱 `docs/MAP.md` §8: 원격 firmware verifier 제거 후 CI가 교차 드리프트를 잡지 못함 |
| selector `0x06` 봉투·revision | `eerraa-qmk-h7s-fw/docs/contract_via.md` (`Canonical for`에 봉투) | `the-via-eerraa/docs/adr/0001-state-sync-protocol.md` (`ls`·헤더 `Status: Accepted`) | 없음. H7S `docs/MAP.md` §7–§8이 교차 검사 없음을 말함 |
| selector `0x07` 진단 wire | `eerraa-qmk-h7s-fw/docs/contract_usb.md` / `contract_via.md` | `the-via-eerraa/docs/adr/0002-h7s-usb-diagnostics.md` | 없음 |
| 메뉴 라벨·설명 문구 | H7S 공식 VIA JSON + `docs/contract_via.md` | `the-via-eerraa/docs/adr/0003-era-menu-help-ui.md` | 없음 |
| 채널·value id 표 | `eerraa-qmk-h7s-fw/docs/MAP.md` §3 (검사기 생성 표) | `the-via-eerraa/docs/MAP.md` §3 | 없음. 앱 쪽 숫자는 `tests/docs-contract.test.ts`가 **앱 소스**와만 대조 |

기능을 한쪽에만 넣으면 안 된다는 규칙은 앱 `AGENTS.md` §4와 H7S `docs/MAP.md` §7에
있다. 검사기가 양쪽을 동시에 열지는 않는다.

`eerraa-54lm20-fw`와의 짝은 이번 채팅에서 확인하지 못했다.

---

## 14. 채택 표

| 저장소 | 규격 버전 | 선언된 이탈 |
| --- | --- | --- |
| `eerraa-agent-docs` | **v1** (이 저장소, 이 태그) | 없음. 규격 원본. 산문은 한국어 |
| `qmk_firmware_eerraa` | 계획이 v1 인용을 커밋 E에 예약. 이 채팅의 커밋 D 트리에는 `eerraa-agent-docs` 인용이 없음 | 계획이 이미 선언한 세 가지 — **장르 디렉터리**, **별도 색인**(`era_active_index.md`), **영어 산문**. 세 가지 모두 커밋 D 트리에서 확인 |
| `the-via-eerraa` | `docs/MAP.md` §9가 「네 저장소 공통 규약」을 서술하나 `eerraa-agent-docs` v1을 가리키지 않음 | 이 채팅에서 확인한 선언 이탈 없음. 7편·flat·한국어·ADR만 `Status`는 이 규격과 맞음 |
| `eerraa-qmk-h7s-fw` | `AGENTS.md`/`docs/MAP.md`에 v1 인용 없음 | 선언된 이탈 문구 없음. 현행은 §12와 충돌하는 graphify 의무가 남아 있음(§12) |
| `eerraa-54lm20-fw` | 저장소에 닿지 못함 (GitHub 404) | 확인 못 함 |

QMK 이탈 세 가지의 확인:

1. **장르 디렉터리** — `keyboards/era/common/docs/{contracts,maps,manuals}/` (`ls`).
2. **별도 색인** — `era_active_index.md`가 `AGENTS.md`와 분리된 `Genre: entry` 문서 (`head`).
3. **영어 산문** — 21편 제목·본문·`Canonical for`가 영어(HID 계약 헤더는 한국어 한 편).
