# 어부바 프로젝트 Back-end 레포지토리입니다. 

<br/><br/>

# 🔉프로젝트 소개

> 어느새 부모님을 바라보는 우리: 돌봄, 계획은 간편하게 비용은 부담없게

정보와 기술의 격차를 해소하고 어디서든 돌봄을 제공한다는 목표로 진행중인 돌봄 서비스입니다. 


<br/><br/>

## 페이지 및 기능 소개
### 1️⃣ 회원가입 및 로그인
서비스를 이용하기 위한 회원가입 및 로그인 기능입니다.

<br/>

### 2️⃣ 예상요양등급
보건복지부에서 실시하는 고령이나 노인성 질병 등으로 일상생활을 혼자서 수행하기 어려운 이들에게 신체활동 및 일상생활 지원 등의 서비스를 제공 받기 위해 필요한 요양등급을 측정할 수 있습니다.

<br/>

### 3️⃣ 복지용구추천 
예상요양등급 측정 결과에 맞는 복지용구를 추천합니다.

<br/>

### 4️⃣ 커뮤니티 
전문가(요양보호사)에게 질문 및 조언을 받거나 유저 간의 소통이 가능합니다.

<br/>

### 5️⃣ 추천 보조금
나이, 거주지역, 예상요양등급 측정 결과에 따라 신청할 수 있는 정부 보조금을 추천합니다.

<br/><br/>

## 사용스택
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"/>

<img src="https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white"/>

<img src="https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white"/> <img src="https://img.shields.io/badge/json%20web%20tokens-323330?style=for-the-badge&logo=json-web-tokens&logoColor=pink"/>

<br><br>

## 개발자
<table>
  <tr>
    <th>Back-end</th>
  </tr>
  <tr>
    <td>
      <a style="display: block;" href="https://github.com/jun-0727">이준영</a>
    </td>
  </tr>
</table>

<br>

## 파일 구조  
```
obuboic
├── accounts         # 계정 관리
│   ├── jwt_handler  // jwt 관리 
│   └── oauth        // 소셜로그인 관리
│       └── kakao
│
├── community        // 커뮤니티 관리
│
├── healths          // 요양등급평가 관리
│
├── sms              // 문자인증 시스템 관리
|
├── common
│   ├── functions.py
│   └── response.py
│
├── config          // 설정 파일 관리
│   ├── settings   
│   ├── urls.py
│   └── wsgi.py
│
└── logs            // 로그 파일 관리
    └── obuboic.log

```

## 
