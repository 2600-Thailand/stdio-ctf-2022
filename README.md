# STDiO CTF 2022

Hi my lovely friends. I wrote gitlab CI to deploy your challenge to the server `45.77.169.171`. Your work is just adding your chall (Docker image) to `server` directory and edit `docker-compose.yml` there. For more detail, I will describe below.

## Naming Convention

### Docker Image Directory

Please follow the following naming convention:

```
[CHALLENGE_CATEGORY]/ch[CHALLENGE_NUMBER]_[CHALLENGE_NAME_WITH_SNAKE_CASE]
```

For example:

```
# CHALLENGE_CATEGORY = crypto
# CHALLENGE_NUMBER = 6
# CHALLENGE_NAME = M1 Pudding
crypto/ch6_m1_pudding
```

### Docker Compose Service Name

Please follow the following naming convention:

```
ch[CHALLENGE_NUMBER]-[CHALLENGE_NUMBER]-[CHALLENGE_NAME_WITH_KEBAB_CASE]
```

For example:

```
# CHALLENGE_CATEGORY = crypto
# CHALLENGE_NUMBER = 6
# CHALLENGE_NAME = M1 Pudding
ch6-crypto-m1-pudding
```

### Challenge Port

Please follow the following naming convention:

```
100[CHALLENGE_NUMBER_LEFT_PAD_0]
```

For example:

```
# CHALLENGE_NUMBER = 6
10006
```

## Challenge Deployment

- Implement challenge and create `Dockerfile` in the directory following [this naming convention](#docker-image-directory) for example, [crypto/ch6_m1_pudding](/server/crypto/ch6_m1_pudding/). (please make sure that your challenge can be built and run perfectly)
- Edit [docker-compose.yml](/server/docker-compose.yml) in order to add your challenge. Set `FLAG` env with `${FLAG_[CHALLENGE_NUMBER_LEFT_PAD_0]}`, forward port following our [this naming convention](#challenge-port) and name challenge server following [this naming convention](#docker-compose-service-name) For example:

```
  ch6-crypto-m1-pudding:
    build: crypto/ch6_m1_pudding
    ports:
      - "10006:1337"
    environment:
      - PROD=true
      - FLAG=${FLAG_06}
```

- Commit and push to `main` branch in this repo
- Wait for CI/CD pipeline to do its job
- Check your challenge at `45.77.169.171`

## Challenge File Upload

- Add your files to `file` directory. (I does not create the naming convention yet. I think it is not necessary)
- Commit and push to `main` branch in this repo
- Wait for CI/CD pipeline to do its job
- Check your files at https://pub-f6b4a5d9d6ff4c2cb57e61cff1114b05.r2.dev/file/

For share challenge source code, you can create bash file started with `run_` to compress source code for you as [this file](/file/run_ch6_m1_pudding.sh).
