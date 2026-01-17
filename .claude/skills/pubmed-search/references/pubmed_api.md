# PubMed E-utilities API Reference

NCBI Entrez Programming Utilities (E-utilities) 상세 가이드

## 1. E-utilities 개요

E-utilities는 NCBI의 Entrez 데이터베이스 시스템에 프로그래밍 방식으로 접근하기 위한 서버 사이드 프로그램입니다.

### Base URL
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

### 주요 엔드포인트

| Endpoint | 기능 | 사용 시점 |
|----------|------|----------|
| esearch.fcgi | 검색어로 UID(PMID) 목록 조회 | 키워드 검색 |
| efetch.fcgi | UID로 전체 레코드 조회 | 논문 상세 정보 |
| esummary.fcgi | UID로 요약 레코드 조회 | 빠른 메타데이터 |
| einfo.fcgi | 데이터베이스 정보 조회 | DB 필드 확인 |
| elink.fcgi | 관련 레코드 링크 조회 | 연관 논문 탐색 |

## 2. ESearch - 검색

### 기본 요청
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
```

### 필수 파라미터
| 파라미터 | 설명 | 예시 |
|---------|------|------|
| db | 데이터베이스 | pubmed |
| term | 검색어 | niacinamide skin |

### 선택 파라미터
| 파라미터 | 설명 | 기본값 |
|---------|------|-------|
| retmax | 반환 최대 수 | 20 |
| retstart | 시작 위치 | 0 |
| retmode | 반환 형식 | xml |
| sort | 정렬 방식 | relevance |
| usehistory | 히스토리 서버 사용 | n |
| datetype | 날짜 유형 | pdat (발행일) |
| mindate | 시작 날짜 | - |
| maxdate | 종료 날짜 | - |

### 예시 요청
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
  ?db=pubmed
  &term=niacinamide+skin
  &retmax=10
  &retmode=json
  &sort=relevance
```

### JSON 응답 예시
```json
{
  "esearchresult": {
    "count": "2847",
    "retmax": "10",
    "retstart": "0",
    "idlist": [
      "34567890",
      "33456789",
      "32345678",
      ...
    ],
    "translationset": [...],
    "querytranslation": "niacinamide[Title/Abstract] AND skin[Title/Abstract]"
  }
}
```

## 3. EFetch - 상세 조회

### 기본 요청
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi
```

### 필수 파라미터
| 파라미터 | 설명 |
|---------|------|
| db | 데이터베이스 (pubmed) |
| id | PMID (콤마로 구분 가능) |

### 선택 파라미터
| 파라미터 | 값 | 설명 |
|---------|---|------|
| rettype | xml | 전체 XML |
| rettype | abstract | 초록 텍스트 |
| rettype | medline | MEDLINE 형식 |
| retmode | xml | XML 형식 |
| retmode | text | 텍스트 형식 |

### 예시 요청
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi
  ?db=pubmed
  &id=34567890,33456789
  &rettype=xml
  &retmode=xml
```

### XML 응답 구조
```xml
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>34567890</PMID>
      <Article>
        <ArticleTitle>...</ArticleTitle>
        <AuthorList>...</AuthorList>
        <Journal>...</Journal>
        <Abstract>...</Abstract>
      </Article>
      <MeshHeadingList>...</MeshHeadingList>
    </MedlineCitation>
    <PubmedData>
      <ArticleIdList>
        <ArticleId IdType="doi">10.xxx/xxx</ArticleId>
        <ArticleId IdType="pmc">PMCxxxxxxx</ArticleId>
      </ArticleIdList>
    </PubmedData>
  </PubmedArticle>
</PubmedArticleSet>
```

## 4. 검색 쿼리 문법

### 필드 태그
| 태그 | 설명 | 예시 |
|-----|------|------|
| [Title] | 제목만 | niacinamide[Title] |
| [Abstract] | 초록만 | skin[Abstract] |
| [Title/Abstract] | 제목+초록 | retinol[Title/Abstract] |
| [MeSH Terms] | MeSH 용어 | dermatology[MeSH Terms] |
| [Author] | 저자명 | Kim J[Author] |
| [Journal] | 저널명 | J Cosmet Dermatol[Journal] |
| [Publication Type] | 논문 유형 | Clinical Trial[Publication Type] |
| [Date - Publication] | 발행일 | 2020:2024[Date - Publication] |

### Boolean 연산자
```
AND - 모두 포함
OR  - 하나 이상 포함
NOT - 제외
```

### 구문 검색
```
"vitamin c"[Title/Abstract]  - 정확한 구문 매칭
vitamin c[Title/Abstract]    - 개별 단어 매칭
```

### 와일드카드
```
*  - 단어 끝에서 자동완성
   예: skin* → skincare, skin-barrier, etc.
```

## 5. 논문 유형 필터

### Publication Type 필터
```
Clinical Trial[Publication Type]
Randomized Controlled Trial[Publication Type]
Meta-Analysis[Publication Type]
Systematic Review[Publication Type]
Review[Publication Type]
Case Reports[Publication Type]
Comparative Study[Publication Type]
Controlled Clinical Trial[Publication Type]
```

### 예시: 임상 시험만 검색
```
niacinamide skin (Clinical Trial[Publication Type] OR Randomized Controlled Trial[Publication Type])
```

## 6. 날짜 필터

### 연도 범위
```
2020:2024[Date - Publication]
2020/01/01:2024/12/31[Date - Publication]
```

### 상대적 날짜
```
last 5 years[Date - Publication]
last 1 year[Date - Publication]
```

## 7. API 키 및 Rate Limiting

### Rate Limits
| 상태 | 초당 요청 수 |
|-----|------------|
| API 키 없음 | 3 |
| API 키 있음 | 10 |

### API 키 등록
1. https://www.ncbi.nlm.nih.gov/account/register/
2. Settings → API Key Management → Create an API Key
3. 요청 시 `api_key` 파라미터 추가

### 예시
```
?db=pubmed&term=...&api_key=YOUR_API_KEY_HERE
```

## 8. Best Practices

### 요청 최적화
1. **usehistory=y**: 대량 검색 시 히스토리 서버 활용
2. **retmax 제한**: 한 번에 최대 10,000개
3. **배치 처리**: 100개씩 분할 요청

### 에러 처리
```python
# 재시도 로직
max_retries = 3
for attempt in range(max_retries):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        break
    except requests.exceptions.RequestException:
        if attempt == max_retries - 1:
            raise
        time.sleep(2 ** attempt)  # 지수 백오프
```

### 캐싱
- 동일 쿼리 결과 로컬 캐싱
- PMID별 논문 정보 캐싱
- 캐시 만료: 24시간 권장

## 9. 관련 리소스

- **E-utilities 공식 문서**: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **PubMed Help**: https://pubmed.ncbi.nlm.nih.gov/help/
- **MeSH Browser**: https://meshb.nlm.nih.gov/
- **NCBI API 키**: https://www.ncbi.nlm.nih.gov/account/settings/
