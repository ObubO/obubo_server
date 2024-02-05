CONVERT_PHYSIC = {
        12: 0.0, 13: 13.19, 14: 22.24, 15: 28.04, 16: 32.38, 17: 35.92, 18: 38.96, 19: 41.68,
        20: 44.18, 21: 46.52, 22: 48.76, 23: 50.93, 24: 53.06, 25: 55.17, 26: 57.30, 27: 59.46, 28: 61.71, 29: 64.06,
        30: 66.59, 31: 69.36, 32: 72.50, 33: 76.22, 34: 81.02, 35: 88.40, 36: 100.0
    }

CONVERT_REHAB = {
    10: 0.0, 11: 11.51, 12: 19.43, 13: 24.72, 14: 28.93, 15: 32.62, 16: 36.06, 17: 39.46, 18: 42.96, 19: 46.69,
    20: 50.72, 21: 54.97, 22: 59.20, 23: 63.19, 24: 66.93, 25: 70.53, 26: 74.16, 27: 78.07, 28: 82.75, 29: 89.57,
    30: 100.0
}

CONVERT_BEHAV = {
    0: 0.0, 1: 15.58, 2: 25.55, 3: 32.10, 4: 37.29, 5: 41.80, 6: 45.95, 7: 49.94, 8: 53.93, 9: 58.08,
    10: 62.59, 11: 67.80, 12: 74.37, 13: 84.37, 14: 100.0
}

CONVERT_RECOG = {
    0: 0.0, 1: 19.71, 2: 33.81, 3: 44.61, 4: 54.78, 5: 65.71, 6: 80.06, 7: 100.0
}

CONVERT_NURSE = {
    0: 0.0, 1: 19.84, 2: 36.9, 3: 47.84, 4: 55.81, 5: 62.53, 6: 68.98, 7: 76.11, 8: 85.86, 9: 100.0
}


class AnalysisDiagram:
    physic_score, recog_score, behav_score, nurse_score, rehab_score = 0, 0, 0, 0, 0
    physic_eat, physic_bath, physic_change, physic_wash = 0, 0, 0, 0
    behav_unstable, behav_chaos, behav_sad, behav_bad = 0, 0, 0, 0
    recog_demen, recog_env, recog_judge = 0, 0, 0
    rehab_right, rehab_left, rehab_low, rehab_up = 0, 0, 0, 0
    nurse_press, nurse_dialy = 0, 0

    def save(self, data):
        global CONVERT_PHYSIC, CONVERT_REHAB, CONVERT_BEHAV, CONVERT_RECOG, CONVERT_NURSE
        physical, recognize, behavior, nursing, rehab = data['physical'], data['recognize'], data['behavior'], data['nursing'], data['rehabilitation']

        # -- 신체기능 설문 점수 저장 --#
        temp = 0
        weight = 12 / 4
        for value in physical.values():
            temp += weight * value

        self.physic_score = CONVERT_PHYSIC[round(temp)]
        self.physic_eat = physical["qa1"]
        self.physic_bath = physical["qa2"]
        self.physic_change = physical["qa3"]
        self.physic_wash = physical["qa4"]

        # -- 인지기능 설문 점수 저장 --#
        temp = 0
        weight = 7 / 3
        for value in recognize.values():
            temp += weight * value

        self.recog_score = CONVERT_RECOG[round(temp)]
        self.recog_demen = recognize["qa1"]
        self.recog_env = recognize["qa2"]
        self.recog_judge = recognize["qa3"]

        # -- 행동변화 설문 점수 저장 --#
        temp = 0
        weight = 14 / 4
        for value in behavior.values():
            temp += weight * value

        self.behav_score = CONVERT_BEHAV[round(temp)]
        self.behav_unstable = behavior["qa1"]
        self.behav_chaos = behavior["qa2"]
        self.behav_sad = behavior["qa3"]
        self.behav_bad = behavior["qa4"]

        # -- 간호처치 설문 점수 저장 --#
        temp = 0
        weight = 9 / 2
        for value in nursing.values():
            temp += weight * value

        self.nurse_score = CONVERT_NURSE[round(temp)]
        self.nurse_press = nursing["qa1"]
        self.nurse_dialy = nursing["qa2"]

        # -- 재활영역 설문 점수 저장 --#
        temp = 0
        weight = 10 / 4
        for value in rehab.values():
            temp += weight * value

        self.rehab_score = CONVERT_REHAB[round(temp)]
        self.rehab_right = rehab["qa1"]
        self.rehab_left = rehab["qa2"]
        self.rehab_low = rehab["qa3"]
        self.rehab_up = rehab["qa4"]

    # == 청결 수형분석도 ==#
    def clean_diagram(self):
        result, score = 0, 9.4

        if self.physic_score <= 34.15:
            if self.physic_score <= 17.72:
                if self.recog_score <= 9.86:
                    result, score = (15, 1.2) if self.physic_score <= 6.59 else (16, 3.0)
                else:
                    result, score = (17, 2.9) if self.recog_score <= 39.21 else (18, 4.1)
            else:
                result, score = (9, 5.3) if self.recog_env == 0 else (10, 8.0)
        else:
            if self.physic_wash != 3:
                result, score = (11, 8.6) if self.physic_bath == 1 else ((19, 9.0) if self.recog_env == 0 else (20, 13.0))
            else:
                result, score = (13, 11.6) if self.physic_bath == 1 else (14, 16.8) if self.rehab_score <= 40.16 else (
                    (21, 16.4) if self.behav_score <= 60.34 else (24, 19.6) if self.rehab_score <= 40.16 else (22, 17.2))

        return score

    # == 배설 수형분석도 ==#
    def bath_diagram(self):
        result, score = 0, 5.6
        if self.physic_change == 1:
            result, score = (1, 3.3)
            if self.physic_bath == 1:
                result, score = (8, 0.9) if self.physic_change == 1 else ((16, 0.5) if self.physic_score == 0 else (
                    (27, 1.2) if self.recog_judge == 0 else ((30, 0.3) if self.behav_score <= 15.58 else (31, 0.7))))
                if result not in (30, 31):
                    result, score = (17, 1.3) if self.physic_score != 0 else (28, 1.0) if self.rehab_low == 1 else (
                        (29, 1.8) if self.recog_env == 0 else ((32, 1.2) if self.recog_env == 0 else (33, 2.5)))
            elif self.physic_bath == 2:
                result, score = (10, 3.8) if self.physic_change == 1 else (11, 8.3)
                if result == 10:
                    result, score = (18, 2.9) if self.physic_bath == 1 else (19, 5.0)
            else:
                result, score = (12, 9.0) if self.behav_unstable == 0 else (13, 15.0)
                if result == 12:
                    result, score = (20, 5.3) if self.physic_wash == 1 else (21, 10.2)
        else:
            result, score = (6, 6.8) if self.physic_eat == 1 else (7, 12.9)
            if result == 7:
                result, score = (14, 11.8) if self.nurse_press == 0 else (
                    (15, 15.8) if self.behav_sad == 0 else ((24, 12.8) if self.physic_bath != 3 else (25, 18.7)))

        return score

    # == 식사 수형분석도 ==#
    def eat_diagram(self):
        result, score = (0, 15.2)
        if self.physic_eat != 3:
            result, score = 1, 12.7
            if self.physic_wash != 1:
                result, score = 3, 10.1
                if self.physic_wash == 1:
                    result, score = (7, 8.3)
                    result, score = (11, 7.1) if self.physic_score <= 6.59 else (12, 9.4)
                else:
                    result, score = 8, 12.9
                    if self.physic_change == 1:
                        result, score = (13, 12.2)
                        result, score = (17, 11.5) if self.behav_unstable == 0 else (18, 14.3)
                    else:
                        result, score = 14, 15.1
            else:
                result, score = 4, 20.1

                if self.physic_bath != 3:
                    result, score = 9, 16.1
                    result, score = (19, 17.5) if self.rehab_score <= 30.77 else (20, 21.4)
                else:
                    result, score = 10, 23.4
        else:
            result, score = 2, 35.6
            result, score = (5, 31.7) if self.rehab_score <= 41.21 else (6, 37.6)

        return score

    # == 기능보조 수형분석도 ==#
    def assist_diagram(self):
        result, score = 0, 7.2
        if self.physic_score <= 47.64:
            result, score = 1, 3.5

            if self.physic_score <= 25.14:
                result, score = 3, 2.0
                if self.physic_score <= 6.59:
                    result, score = 7, 1.2
                else:
                    result, score = 8, 2.7
            else:
                result, score = 4, 6.0
                if self.physic_bath == 1:
                    result, score = 9, 4.9

                    if self.physic_wash != 3:
                        result, score = 15, 4.3

                        if self.rehab_right == 1:
                            result, score = 21, 3.6
                        else:
                            result, score = 22, 6.0
                    else:
                        result, score = 16, 6.8
                else:
                    result, score = 10, 7.8

                    if self.behav_bad == 0:
                        result, score = 17, 6.6
                    else:
                        result, score = 18, 9.2
        else:
            result, score = 2, 13.3

            if self.physic_wash != 3:
                result, score = 5, 8.6

                if self.physic_change != 3:
                    result, score = 11, 7.9

                    if self.behav_score <= 28.83:
                        result, score = 19, 6.4
                    else:
                        result, score = 20, 9.3
                else:
                    result, score = 12, 10.9
            else:
                result, score = 6, 15.1

                if self.nurse_press == 0:
                    result, score = 13, 14.0
                else:
                    result, score = 14, 18.7

        return score

    # == 행동변화대응 수형분석도 ==#
    def behav_diagram(self):
        result, score = 0, 1.3
        if self.behav_score <= 34.69:
            result, score = (3, 0.7) if self.behav_score <= 7.79 else (4, 1.1)
            if self.behav_score <= 7.79:
                result, score = (7, 0.6) if self.physic_score <= 17.71 else (8, 0.8)
            else:
                result, score = (9, 0.9) if self.recog_score <= 60.24 else (10, 1.3)
        else:
            result, score = (5, 1.4) if self.recog_score <= 39.21 else (
                (11, 1.6) if self.behav_unstable == 0 else (12, 2.6))
            if result == 12:
                result, score = (13, 2.2) if self.physic_wash != 3 else (14, 3.2)

        return score

    # == 간접지원 수형분석도 ==#
    def support_diagram(self):
        result, score = 0, 18.9
        if self.physic_score <= 25.14:
            result, score = (3, 12.5) if self.physic_score <= 6.59 else (4, 16.9)
        else:
            result, score = (5, 20.3) if self.behav_unstable == 0 else (6, 26.1)
            if result == 5:
                result, score = (7, 17.6) if self.physic_bath == 1 else (
                    (11, 19.8) if self.behav_sad == 0 else (12, 23.0))
                if result == 11:
                    result, score = (13, 17.3) if self.physic_eat == 1 else (
                        (15, 19.7) if self.behav_chaos == 0 else (16, 23.6))
                elif result == 12:
                    result, score = (14, 21.0) if self.physic_eat == 1 else (
                        (15, 19.7) if self.behav_chaos == 0 else (16, 23.6))
            else:
                result, score = (9, 21.7) if self.behav_score <= 56 else (10, 28.4)

        return score

    # == 간호처치 수형분석도 ==#
    def nurse_diagram(self):
        result, score = 0, 9.3
        if self.nurse_press == 0:
            if self.nurse_score == 0:
                result, score = (3, 8.3) if self.behav_chaos == 0 else (
                    (8, 7.6) if self.rehab_left == 1 and self.behav_unstable == 0 else (9, 9.7))
            elif self.nurse_score <= 19.84:
                result, score = (4, 9.6)
            else:
                result, score = (5, 14.6)
        else:
            if self.physic_eat != 3:
                result, score = (6, 12.4) if self.physic_wash != 3 else (10, 9.6) if self.physic_wash != 3 else (
                    11, 14.7)
            else:
                result, score = (7, 22.5)

        return score

    # == 재활훈련 수형분석도 ==#
    def rehab_diagram(self):
        result, score = 0, 4.3
        if self.rehab_score == 0:
            result, score = (4, 2.5) if self.behav_unstable == 0 else (5, 3.7)
        elif self.rehab_score <= 39.46:
            result, score = (6, 4.6) if self.physic_wash != 3 else (
                (10, 4.1) if self.physic_change == 1 else (11, 6.3) if self.physic_change != 3 else (
                    7, 3.1) if self.physic_change != 3 else (12, 2.1) if self.physic_change != 3 else (13, 4.2))
            if result == 10 and self.physic_change == 1:
                result, score = (14, 4.5) if self.recog_env == 0 else (15, 3.2) if self.recog_env != 0 else (
                    16, 4.0) if self.physic_wash == 1 else (17, 5.7)
                if result == 14 and self.recog_env == 0:
                    result, score = (16, 4.0) if self.physic_wash == 1 else (17, 5.7)
                elif result == 15 and self.recog_env != 0:
                    result, score = (18, 3.8) if self.physic_change == 1 else (19, 2.7)
        else:
            result, score = (8, 4.8) if self.behav_sad == 0 else (9, 6.3)

        return score

    # == 등급평가 ==#
    def get_rate(self, score):
        rate = 0

        if score >= 95:
            rate = "어르신의 예상 장기요양등급은 1~2 등급입니다."
            detail = {
                "option1": "요양원 등 이용 시 전체 비용의 20%인 487,170원 (1개월 기준)으로 이용하실 수 있습니다.",
                "option2": "방문간호, 방문요양 등 이용 시 전체 비용의 15%인 3,618원 (1시간 기준)으로 이용하실 수 있습니다.",
                "option3": "해당 등급은 데이케어센터 이용이 불가합니다."
            }
        elif score >= 75:
            rate = "어르신의 예상 장기요양등급은 2~3 등급입니다."
            detail = {
                "option1": "요양원 등 이용 시 전체 비용의 20%인 455,850원 (1개월 기준)으로 이용하실 수 있습니다.",
                "option2": "방문간호, 방문요양 등 이용 시 전체 비용의 15%인 3,618원 (1시간 기준)으로 이용하실 수 있습니다.",
                "option3": "전체 비용의 15%인 170,280원 (20일 기준)으로 이용하실 수 있습니다"
            }
        elif score >= 60:
            rate = "어르신의 예상 장기요양등급은 3~4 등급입니다."
            detail = {
                "option1": "요양원 등 이용 시 전체 비용의 20%인 442,800원 (1개월 기준)으로 이용하실 수 있습니다.",
                "option2": "방문간호, 방문요양 등 이용 시 전체 비용의 15%인 3,618원 (1시간 기준)으로 이용하실 수 있습니다.",
                "option3": "전체 비용의 15%인 165,640원 (20일 기준)으로 이용하실 수 있습니다"
            }
        elif score >= 51:
            rate = "어르신의 예상 장기요양등급은 4~5 등급입니다."
            detail = {
                "option1": "요양원 등 이용 시 전체 비용의 20%인 442,800원 (1개월 기준)으로 이용하실 수 있습니다.",
                "option2": "방문간호, 방문요양 등 이용 시 전체 비용의 15%인 3,618원 (1시간 기준)으로 이용하실 수 있습니다.",
                "option3": "전체 비용의 15%인 160,920원 (20일 기준)으로 이용하실 수 있습니다"
            }
        elif score >= 45 and self.recog_demen == 1:
            rate = "어르신의 예상 장기요양등급은 5~인지지원 등급입니다."
            detail = {
                "option1": "장기요양 등급 평가기관에 문의 후 확인가능합니다.",
                "option2": "장기요양 등급 평가기관에 문의 후 확인가능합니다.",
                "option3": "장기요양 등급 평가기관에 문의 후 확인가능합니다."
            }
        else:
            rate = "간소화 평가로 판단할 수 없습니다."
            detail = {
                "option1": "회원가입 후 장기요양등급평가(상세) 기능을 이용해보세요!",
                "option2": "회원가입하기",
                "option3": "홈으로 돌아가기"
            }

        result = {
            "rate": rate,
            "detail": detail,
        }

        return result
