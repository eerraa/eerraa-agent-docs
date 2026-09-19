# 중앙 규약 유지보수

이 레포는 문서 작성 표준이다. 소비 레포의 제품 계약·현재 구현·채택 상태를 소유하지 않는다.

## 진입

root/branch/HEAD/status와 관련 diff를 확인하고 사용자 변경을 보존한다. [규약](AGENT_DOCS_CONVENTION.md)의 관련 절만 읽는다. 채택 절차를 바꿀 때만 [ADOPTION](ADOPTION.md)을 추가로 읽는다.

| 변경 | 소유 위치 | 확인 |
|---|---|---|
| 공통 원칙·경계 | [규약](AGENT_DOCS_CONVENTION.md) | 요구 보존·소스 복제·읽기 비용 검토 |
| 채택·분할 정비 절차 | [ADOPTION](ADOPTION.md) | 로컬 독립성·완료 조건 검토 |
| 사용자 진입 | [README](README.md) | 링크와 역할 중복 검토 |
| 중앙 구조 검사 | [검사기](scripts/check.py), [시험](tests/test_check.py) | 정상·음성 fixture |
| CI | [workflow](.github/workflows/docs.yml) | 로컬과 같은 명령·읽기 권한만 |

## 경계

- 짧은 규칙·표·예시로 작성한다. 삭제한 조사 서사, 소비 레포별 현황표, 세션 프롬프트, 완료 기록을 되살리지 않는다.
- 요구사항·안전·호환성을 실제 구현과 혼동하지 않는다. 문서 축소는 요구 완화 권한이 아니다.
- 형식 통일을 위해 소비 레포에 새 문서·공유 패키지·동기화·전역 훅을 강요하지 않는다.
- 한국어 산문, 기술 식별자는 원문. UTF-8/LF. 주석은 비자명한 이유만 쓴다.
- 검사기는 중앙 레포 전용이다. 범용 Markdown 파서·자연어 판정기·소비 레포 스캐너로 확대하지 않는다.
- 임시 산출물은 ignored `.local/`에 둔다. 인증 정보·비공개 소비 레포 내용은 공개 트리에 넣지 않는다.
- 검증된 관심사만 commit한다. 요청 없는 push/tag/release·외부 레포 수정·전역 설정 변경은 하지 않는다. 공개 태그를 이동하지 않는다.

## 검증과 종료

```sh
python -X utf8 scripts/check.py
python -X utf8 -m unittest discover -s tests -v
git diff --check
```

최종 diff·status·남은 작업을 확인한다. 변경 범위, 실제 검증 결과, commit/원격 반영 여부, 미검증 한계를 응답에 보고한다. 별도 보고 문서는 만들지 않는다.
