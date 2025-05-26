# beomdo's ML-DL blog

데이터 분석, 머신러닝, 프로그래밍 관련 학습 내용을 기록하고 공유합니다.

[➡️ **블로그 바로가기**](https://beomdo-park.github.io)

## ✨ 기술 스택

[![Quarto](https://img.shields.io/badge/Quarto-4B8BBE?style=for-the-badge&logo=Quarto&logoColor=white)](https://quarto.org/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-181717?style=for-the-badge&logo=github&logoColor=white)](https://pages.github.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)

---

## 🗂️ 레포지토리 구조

![레포지토리 구조](assets/repo_structure.png)

## 🚀 배포 과정

![배포 과정](assets/deployment_process.png)

### 🔗 구조와 배포의 연결

이 블로그의 배포 과정은 위 두 다이어그램에 나타난 레포지토리 구조와 긴밀하게 연결되어 있습니다.

1.  **변경사항 발생 및 푸시**: 로컬에서 블로그 게시물(`posts/`)을 작성하거나, 스타일(`styles.css`), 또는 블로그 설정(`_quarto.yml`, `index.qmd`)을 수정한 후, 변경 사항을 `main` 브랜치로 `Git Push`합니다.
2.  **워크플로우 실행**: 이 푸시는 `.github/workflows/` 폴더 내의 `publish.yml` 파일에 정의된 GitHub Actions 워크플로우를 자동으로 트리거합니다.
3.  **빌드**: GitHub Actions는 `main` 브랜치의 최신 코드를 가져와 Quarto 프로젝트를 빌드합니다. 이 과정에서 `_quarto.yml`이 프로젝트 전체 설정을 담당하고, `posts/`의 `.qmd` 파일들이 개별 게시물로 변환됩니다. 필요한 경우 `scripts/` 내의 코드가 빌드 과정에 사용될 수 있습니다.
4.  **결과물 생성 및 배포**: 빌드가 완료되면, 생성된 웹사이트 파일들은 `docs/` 폴더 (레포지토리 구조 다이어그램의 '빌드 결과' 폴더)에 해당하는 내용으로 구성됩니다. `publish.yml` 워크플로우는 이 결과물을 `gh-pages` 브랜치로 푸시합니다.
5.  **블로그 게시**: GitHub Pages는 `gh-pages` 브랜치의 내용을 자동으로 감지하여 `https://beomdo-park.github.io` 주소로 블로그를 웹에 게시합니다.

이처럼 레포지토리의 각 구성 요소는 체계적인 배포 자동화 과정을 통해 최종적으로 여러분이 보시는 블로그로 완성됩니다.
