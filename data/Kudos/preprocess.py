import os
import cv2
import numpy as np

def extract_white(input_image_path, output_image_path):
    # 이미지 불러오기
    image = cv2.imread(input_image_path)

    # BGR에서 HSV로 변환
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 초록색 범위 지정
    lower_green = np.array([40, 40, 40], dtype=np.uint8)
    upper_green = np.array([80, 255, 255], dtype=np.uint8)

    # 초록색 부분 추출
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    # 내부의 흰색 범위 지정 (HSV)
    lower_white_inner_hsv = np.array([0, 0, 200], dtype=np.uint8)
    upper_white_inner_hsv = np.array([255, 100, 255], dtype=np.uint8)

    # 내부의 흰색 부분 추출
    white_mask_inner = cv2.inRange(hsv, lower_white_inner_hsv, upper_white_inner_hsv)
    
    # 외부의 흰색 범위 지정 (HSV)
    lower_white_outer_hsv = np.array([0, 0, 190], dtype=np.uint8)
    upper_white_outer_hsv = np.array([255, 40, 255], dtype=np.uint8)

    # 외부의 흰색 부분 추출
    white_mask_outer = cv2.inRange(hsv, lower_white_outer_hsv, upper_white_outer_hsv)

    # 내부와 외부의 흰색을 합침
    white_mask_combined = cv2.bitwise_or(white_mask_inner, white_mask_outer)

    # 원본 이미지에서 흰색 부분만 남기기
    result_image = cv2.bitwise_and(image, image, mask=white_mask_combined)

    # 새로운 이미지 저장
    cv2.imwrite(output_image_path, result_image)

def process_images(input_folder, output_folder):
    # 입력 폴더의 모든 파일 목록 가져오기
    input_files = os.listdir(input_folder)

    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 모든 이미지에 대해 변환 수행
    for input_file in input_files:
        input_path = os.path.join(input_folder, input_file)
        output_path = os.path.join(output_folder, input_file)

        # 이미지 변환 함수 호출
        extract_white(input_path, output_path)

# 사용 예시
input_folder = 'received_images'  # 입력 이미지 폴더 경로
output_folder = 'processed_images'  # 결과 이미지 저장 폴더 경로
process_images(input_folder, output_folder)
