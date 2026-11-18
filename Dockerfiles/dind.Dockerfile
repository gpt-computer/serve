FROM docker:24.0-git

RUN apk add --no-cache curl bash make

CMD ["bash"]
