# Toolformer Demonstration Notebook

**언어 선택 / Language Selection:**

- [🇰🇷 한국어 (Korean)](README.ko.md)
- [🇺🇸 English](README.md)

## 개요  
[이 Jupyter 노트북](https://github.com/limJhyeok/toolformer-experiment/blob/main/jupyter.ipynb)은 **Toolformer** 접근 방식을 시연합니다. 이 접근법에서는 언어 모델(GPT-J)을 API 호출 기능과 통합하여 외부 정보가 필요한 작업을 수행할 수 있는 능력을 향상시킵니다. 텍스트 생성 중에 API 호출을 삽입하고 해당 응답을 활용하여 모델이 실시간 데이터를 동적으로 통합할 수 있습니다.

## 주요 특징  
- **API 호출 통합**: 외부 정보가 필요한 텍스트에 API 호출을 자동으로 삽입합니다.  
- **동적 API 실행**: API 호출을 실행하고 그 결과를 출력 텍스트에 통합합니다.  
- **Loss 기반 평가/필터링**: API 호출 결과가 있는 텍스트와 없는 텍스트의 loss 값을 비교하여 파인튜닝에 적합한 데이터셋을 결정합니다.  
- **모델 파인튜닝**: 선택된 데이터셋을 사용하여 GPT-J를 파인튜닝하여 API를 인식하는 텍스트 생성을 개선합니다.  
- **반복적 추론**: API 결과가 후속 텍스트 생성에 동적으로 영향을 미치는 반복적 프로세스를 구현합니다.

## 사용법  
### 사전 요구 사항  
1. 필요한 Python 라이브러리를 설치합니다:  
   ```bash
   pip install torch transformers
   ```
   
2. 최적의 성능을 위해 **GPU**에 접근 가능해야 합니다.

### 노트북 워크플로우  
1. **설정**:  
   - Hugging Face Transformers 라이브러리에서 GPT-J 모델과 토크나이저를 로드합니다.  
   - 동적 날짜 관련 쿼리를 위한 맞춤형 `Calendar` API 도구를 정의합니다.  

2. **프롬프트 및 데이터 준비**:  
   - API 호출이 필요한 경우 통합하도록 모델에 지시하는 프롬프트를 정의합니다.  
   - API 호출 생성을 위한 예제 입력 데이터를 제공합니다.

3. **API 호출 생성 및 실행**:  
   - 모델은 외부 정보가 필요한 경우 `[Calendar()]` API 호출을 삽입한 텍스트를 생성합니다.  
   - API 호출을 실행하고 결과를 텍스트에 다시 통합합니다.

4. **Loss 계산**:  
   - 세 가지 텍스트 변형에 대한 Loss 값을 계산합니다:
     - API 결과 포함 (`[Calendar() -> Today is Thursday, November 30, 2023.]`)
     - API 결과 미포함 (`[Calendar()]`)
     - 일반 텍스트 (API 호출 없음)  
   - loss를 비교하여 fine-tuning에 가장 적합한 데이터셋을 필터링합니다.

5. **fine-tuning**:  
   - loss 비교에 기반한 fine-tuning 데이터셋을 생성합니다.  
   - API를 인식하는 텍스트 생성을 개선하기 위해 GPT-J 모델을 fine-tuning합니다.

6. **추론**:  
   - fine-tuning된 모델에 새 입력을 제공합니다.  
   - 모델이 API 호출(예: `->`)을 생성하면 API 호출을 실행하고 결과를 통합한 뒤 반복적으로 디코딩을 계속 진행합니다.

---

## 예시  
### 입력:  
```text
The store is never open on the weekend, so today it is closed.
```

### 출력:  
```text
The store is never open on the [Calendar() -> Today is Saturday, November 25, 2023.] weekend, so today it is closed.
```

## 주요 내용  
- **Loss 기반 필터링**: API 결과를 포함하면 Loss가 개선되는지 여부를 통해 데이터셋을 필터링합니다:
  ```bash
  # e.g.,
  API 결과 포함 Loss: 2.84
  API 결과 미포함 Loss: 2.98
  일반 텍스트 (API 호출 없음) Loss: 3.83
  ```
  ```python
  # api_with_result_output.loss: 2.84
  # api_without_result_output.loss: 2.98
  # plain_output.loss: 3.83
  # filtering_threshold: 사용자 정의(e.g., 1.0)

  if min(api_without_result_output.loss, plain_output.loss) - api_with_result_output.loss >= filtering_threshold:
    finetune_dataset = including_API_without_result + next_words
  else:
    finetune_dataset = plain_text + next_words
  ```
- **동적 API 호출**: 텍스트 생성 중 모델이 도구(tool)와 원활하게 상호 작용할 수 있도록 합니다.  
- **사용자 정의 API**: `Calendar` 외의 다른 API를 쉽게 확장할 수 있습니다.

---

## 학습 목표  
1. 외부 API 도구를 언어 모델에 통합하는 방법을 이해합니다.  
2. API 호출의 영향을 평가하기 위해 손실 기반 필터링을 탐구합니다.  
3. 동적 도구 지원 텍스트 생성을 위해 언어 모델을 파인튜닝합니다.  
4. 실시간 API 활용을 위한 반복 추론 파이프라인을 구현합니다.

## 참고 자료  
1. [Toolformer: Language Models Can Teach Themselves to Use Tools (원본 논문)](https://arxiv.org/abs/2302.04761)  
2. [lucidrains/toolformer-pytorch](https://github.com/lucidrains/toolformer-pytorch)

## 노트  
이 노트북은 **Toolformer** 원리를 소개하기 위한 것입니다. 데이터베이스 쿼리, 실시간 날씨 업데이트 또는 지식 검색 시스템과 같은 특정 사용 사례를 처리하기 위해 추가 API 및 맞춤형 파이프라인으로 확장할 수 있습니다.
