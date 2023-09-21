# 기반 이미지로 Nginx를 사용합니다.
FROM nginx:latest

# 컨테이너 포트 설정 (80번 포트 사용)
EXPOSE 80

# 컨테이너가 시작될 때 실행할 명령을 설정합니다.
CMD ["nginx", "-g", "daemon off;"]