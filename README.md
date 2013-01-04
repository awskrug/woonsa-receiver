# Woonsa

본 프로젝트는, 한국의 Amazon Web Service 사용자들을 위해 Tokyo Region과 한국의 여러 ISP간의 네트웍 품질을 모니터링하는 프로젝트입니다.

Woonsa(운사, 雲師)라는 이름은, 단군 신화에서 환웅이 거느린 구름을 담당하는 운사에서 따온 이름으로
클라우드 서비스의 상태를 모니터링하는데서 착안한 이름입니다.

# Receiver

Configuration
--------------
    emitter:
	    dynamodb:
	        aws_access_key_id: <your acceess key>
	        aws_secret_access_key: <your secret key>
	        aws_region: ap-northeast-1
	        aws_dynamo_db_schema: woonsa

	    carbon:
	        host: localhost
	        port: 2003

Dynamo DB
----------

`client_id`를 `hash key`로 `ts`를 `range key`로 하는 table을 만들어야 합니다.


# Agent

`collect.example.sh`를 참고합니다.

	W_ID: 구분 key
	W_HOST: Receiver 주소
	W_PORT: Receiver 포트
	M_COUNT: 데이터 수집 횟수(mtr --c)
	M_OPTS: mtr 수행 옵션
	M_BIN: mtr 경로

