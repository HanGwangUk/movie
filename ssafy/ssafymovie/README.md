# SSAFY 최종 프로젝트

## git을 이용한 공동 작업공간

> git branch 사용
>
> 한광욱 : brchA
> 이예림 : brchB



### branch 명령어

```bash
#브랜치 생성
$git branch { 브랜치명 }

#브랜치 이동
$git checkout {브랜치명}

#브랜치 확인
$git branch

[참고사이트]
https://victorydntmd.tistory.com/91
```



### git 하루 루틴

> ##### 아침
>
> 각자 브랜치에서 전 날 올린 master file pull하기

```bash
$git checkout brchB
$git pull origin master
```

> ##### 틈틈이
>
> 각자 브랜치에서 작업 후 

```bash
$git add.
$git commit -m '메세지'
$git push origin brchB
```

> ##### 자기 전
>
> master로 이동 후 각자 브랜치에서 작업한 것 pull, push하기

```bash
$git checkout master
$git pull origin brchB
$git push origin master

#pull했을 때 충돌오류 발생 => 충돌 해결 후 push
```



## 파일 구조

```

```



## 명세서

### 1단계 : 필수구현

* JSON파일 받아오기

* index.html
  * JSON image받아오기
  * 







---

## 스케줄링

#### 6월 11일  | 목

- [ ] accounts 구현하기
- [ ] JSON데이터 받아오기

#### 6월 12일   | 금

- [ ] movie쪽 만들기
- [ ] 알고리즘 만들기
- [ ] 그 전까지한거 체크

#### 6월 13일  |  토

- [ ] bootstrap으로 꾸미기
- [ ] 추가 사항 넣기(검색창) - 되면
- [ ] UCC 어떤식으로 만들지 구상하기

#### 6월 14일   |  일

- [ ] bootstrap으로 꾸미기
- [ ] UCC 만들기



