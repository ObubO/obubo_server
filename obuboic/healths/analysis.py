import math

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

CLEAN_DIC = {0: 9.4, 1: 3.9, 2: 14.3, 3: 2.6, 4: 6.5, 5: 11.2, 6: 16.4, 7: 1.7, 8: 3.4, 9: 5.3, 10: 8.0, 11: 8.6,
             12: 11.9, 13: 11.6, 14: 16.8, 15: 1.2, 16: 3.0, 17: 2.9, 18: 4.1, 19: 9.0, 20: 13.0, 21: 16.4, 22: 17.2,
             23: 15.4, 24: 19.6}
BATH_DIC = {0: 5.6, 1: 3.3, 2: 11.9, 3: 1.2, 4: 4.8, 5: 10.8, 6: 6.8, 7: 12.9, 8: 0.9, 9: 2.6, 10: 3.8, 11: 8.3,
            12: 9.0, 13: 15.0, 14: 11.8, 15: 15.8, 16: 0.5, 17: 1.3, 18: 2.9, 19: 5.0, 20: 5.3, 21: 10.2, 22: 8.8,
            23: 12.5, 24: 12.8, 25: 18.7, 26: 0.4, 27: 1.2, 28: 1.0, 29: 1.8, 30: 0.3, 31: 0.7, 32: 1.2, 33: 2.5}
EAT_DIC = {0: 15.2, 1: 12.7, 2: 35.6, 3: 10.1, 4: 20.1, 5: 31.7, 6: 37.6, 7: 8.3, 8: 12.9, 9: 16.1, 10: 23.4, 11: 7.1,
           12: 9.4, 13: 12.2, 14: 15.1, 15: 13.9, 16: 18.7, 17: 11.5, 18: 14.3, 19: 17.5, 20: 21.4}
ASSIST_DIC = {0: 7.2, 1: 3.5, 2: 13.3, 3: 2.0, 4: 6.0, 5: 8.6, 6: 15.1, 7: 1.2, 8: 2.7, 9: 4.9, 10: 7.8, 11: 7.9,
              12: 10.9, 13: 14.0, 14: 18.7, 15: 4.3, 16: 6.8, 17: 6.6, 18: 9.2, 19: 6.4, 20: 9.3, 21: 3.6, 22: 6.0}
BEHAV_DIC = {0: 1.3, 1: 0.9, 2: 1.9, 3: 0.7, 4: 1.1, 5: 1.4, 6: 2.0, 7: 0.6, 8: 0.8, 9: 0.9, 10: 1.3, 11: 1.6, 12: 2.6,
             13: 2.2, 14: 3.2}
SUPPROT_DIC = {0: 18.9, 1: 14.7, 2: 21.5, 3: 12.5, 4: 16.9, 5: 20.3, 6: 26.1, 7: 17.6, 8: 21.2, 9: 21.7, 10: 28.4,
               11: 19.8, 12: 23.0, 13: 17.3, 14: 21.0, 15: 19.7, 16: 23.6}
NURSE_DIC = {0: 9.3, 1: 8.7, 2: 15.4, 3: 8.3, 4: 9.6, 5: 14.6, 6: 12.4, 7: 22.5, 8: 7.6, 9: 9.7, 10: 9.6, 11: 14.7,
             12: 7.1, 13: 9.5, 14: 6.7, 15: 8.1, 16: 7.4, 17: 11.6}
REHAB_DIC = {0: 4.3, 1: 3.0, 2: 4.3, 3: 5.5, 4: 2.5, 5: 3.7, 6: 4.6, 7: 3.1, 8: 4.8, 9: 6.3, 10: 4.1, 11: 6.3, 12: 2.1,
             13: 4.2, 14: 4.5, 15: 3.2, 16: 4.0, 17: 5.7, 18: 3.8, 19: 2.7}


class AnalysisDiagram:
    physic_score, recog_score, behav_score, nurse_score, rehab_score = 0, 0, 0, 0, 0
    physic_clothes, physic_wash_face, physic_brush_teeth, physic_take_bath, physic_eat, physic_change_position, physic_stand_sit, physic_move_sit, physic_room_out, physic_use_bathroom, physic_control_defecation, physic_control_fee = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    recog_demen, recog_short_memory, recog_date, recog_place, recog_age, recog_indicate, recog_judge, recog_commu = 0, 0, 0, 0, 0, 0, 0, 0
    behav_delusion, behav_hallucination, behav_sad, behav_chaos, behav_resistance, behav_unstable, behav_lost, behav_bad_aggressive, behav_go_outside, behav_break, behav_bad_behav, behav_hide, behav_bad_dress, behav_bad_bath = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    nurse_bronchial, nurse_suction, nurse_oxygen, nurse_press, nurse_camouflage, nurse_pain, nurse_fee, nurse_jangru, nurse_dialysis = 0, 0, 0, 0, 0, 0, 0, 0, 0
    rehab_right_up, rehab_right_down, rehab_left_up, rehab_left_down = 0, 0, 0, 0
    rehab_join_shoulder, rehab_joint_elbow, rehab_joint_wrist, rehab_joint_hip, rehab_joint_knee, rehab_joint_ankle = 0, 0, 0, 0, 0, 0

    def save(self, data):
        global CONVERT_PHYSIC, CONVERT_REHAB, CONVERT_BEHAV, CONVERT_RECOG, CONVERT_NURSE
        physical, recognize, behavior, nursing, rehab = data['physical'], data['recognize'], data['behavior'], data[
            'nursing'], data['rehabilitation']

        # -- 신체기능 설문 점수 저장 --#
        score = 0
        for value in physical.values():
            score += int(value)

        self.physic_score = CONVERT_PHYSIC[score]

        self.physic_clothes = int(physical["physicalQuestionnaire1"])
        self.physic_wash_face = int(physical["physicalQuestionnaire2"])
        self.physic_brush_teeth = int(physical["physicalQuestionnaire3"])
        self.physic_take_bath = int(physical["physicalQuestionnaire4"])
        self.physic_eat = int(physical["physicalQuestionnaire5"])
        self.physic_change_position = int(physical["physicalQuestionnaire6"])
        self.physic_stand_sit = int(physical["physicalQuestionnaire7"])
        self.physic_move_sit = int(physical["physicalQuestionnaire8"])
        self.physic_room_out = int(physical["physicalQuestionnaire9"])
        self.physic_use_bathroom = int(physical["physicalQuestionnaire10"])
        self.physic_control_defecation = int(physical["physicalQuestionnaire11"])
        self.physic_control_fee = int(physical["physicalQuestionnaire12"])

        # -- 인지기능 설문 점수 저장 --#
        score = 0
        for value in recognize.values():
            score += int(value)

        self.recog_score = CONVERT_RECOG[score]

        self.recog_demen = int(recognize["recognizeQuestionnaire1"])
        self.recog_short_memory = int(recognize["recognizeQuestionnaire2"])
        self.recog_date = int(recognize["recognizeQuestionnaire3"])
        self.recog_place = int(recognize["recognizeQuestionnaire4"])
        self.recog_age = int(recognize["recognizeQuestionnaire5"])
        self.recog_indicate = int(recognize["recognizeQuestionnaire6"])
        self.recog_judge = int(recognize["recognizeQuestionnaire7"])
        self.recog_commu = int(recognize["recognizeQuestionnaire8"])

        # -- 행동변화 설문 점수 저장 --#
        score = 0
        for value in behavior.values():
            score += int(value)

        self.behav_score = CONVERT_BEHAV[score]

        self.behav_delusion = int(behavior["behaviorQuestionnaire1"])
        self.behav_hallucination = int(behavior["behaviorQuestionnaire2"])
        self.behav_sad = int(behavior["behaviorQuestionnaire3"])
        self.behav_chaos = int(behavior["behaviorQuestionnaire4"])
        self.behav_resistance = int(behavior["behaviorQuestionnaire5"])
        self.behav_unstable = int(behavior["behaviorQuestionnaire6"])
        self.behav_lost = int(behavior["behaviorQuestionnaire7"])
        self.behav_bad_aggressive = int(behavior["behaviorQuestionnaire8"])
        self.behav_go_outside = int(behavior["behaviorQuestionnaire9"])
        self.behav_break = int(behavior["behaviorQuestionnaire10"])
        self.behav_bad_behav = int(behavior["behaviorQuestionnaire11"])
        self.behav_hide = int(behavior["behaviorQuestionnaire12"])
        self.behav_bad_dress = int(behavior["behaviorQuestionnaire13"])
        self.behav_bad_bath = int(behavior["behaviorQuestionnaire14"])

        # -- 간호처치 설문 점수 저장 --#
        score = 0
        for value in nursing.values():
            score += int(value)

        self.nurse_score = CONVERT_NURSE[score]

        self.nurse_bronchial = int(nursing["nursingQuestionnaire1"])
        self.nurse_suction = int(nursing["nursingQuestionnaire2"])
        self.nurse_oxygen = int(nursing["nursingQuestionnaire3"])
        self.nurse_press = int(nursing["nursingQuestionnaire4"])
        self.nurse_camouflage = int(nursing["nursingQuestionnaire5"])
        self.nurse_pain = int(nursing["nursingQuestionnaire6"])
        self.nurse_fee = int(nursing["nursingQuestionnaire7"])
        self.nurse_jangru = int(nursing["nursingQuestionnaire8"])
        self.nurse_dialysis = int(nursing["nursingQuestionnaire9"])

        # -- 재활영역 설문 점수 저장 --#
        score = 0
        for value in rehab.values():
            score += int(value)

        self.rehab_score = CONVERT_REHAB[score]

        self.rehab_right_up = int(rehab["rehabilitationQuestionnaire1"])
        self.rehab_right_down = int(rehab["rehabilitationQuestionnaire2"])
        self.rehab_left_up = int(rehab["rehabilitationQuestionnaire3"])
        self.rehab_left_down = int(rehab["rehabilitationQuestionnaire4"])
        self.rehab_join_shoulder = int(rehab["rehabilitationQuestionnaire5"])
        self.rehab_joint_elbow = int(rehab["rehabilitationQuestionnaire6"])
        self.rehab_joint_wrist = int(rehab["rehabilitationQuestionnaire7"])
        self.rehab_joint_hip = int(rehab["rehabilitationQuestionnaire8"])
        self.rehab_joint_knee = int(rehab["rehabilitationQuestionnaire9"])
        self.rehab_joint_ankle = int(rehab["rehabilitationQuestionnaire10"])

    def clean_diagram(self):
        if self.physic_score <= 34.15:
            if self.physic_score <= 17.72:
                if self.recog_score <= 9.86:
                    result = 15 if self.physic_score <= 6.59 else 16
                else:
                    result = 17 if self.recog_score <= 39.21 else 18
            else:
                result = 9 if self.recog_age == 0 else 10
        else:
            if self.physic_brush_teeth != 3:
                if self.physic_use_bathroom == 1:
                    result = 11
                else:
                    result = 19 if self.recog_date == 0 else 20
            else:
                if self.physic_use_bathroom == 1:
                    result = 13
                else:
                    if self.rehab_score <= 40.16:
                        result = 23 if self.behav_score <= 60.34 else 24
                    else:
                        result = 22

        return CLEAN_DIC[result]

    def bath_diagram(self):
        if self.physic_change_position == 1:
            if self.physic_control_fee is 1:
                if self.physic_clothes is 1:
                    if self.physic_score is 0:
                        if self.recog_judge is 0:
                            result = 30 if self.behav_score <= 15.58 else 31
                        else:
                            result = 27
                    else:
                        if self.rehab_joint_knee is 1:
                            result = 28
                        else:
                            result = 32 if self.recog_date is 0 else 33
                else:
                    result = 9
            elif self.physic_control_fee is 2:
                if self.physic_move_sit is 1:
                    result = 18 if self.physic_use_bathroom is 1 else 19
                else:
                    result = 11
            else:
                if self.behav_go_outside is 0:
                    result = 20 if self.physic_wash_face is 1 else 21
                else:
                    result = 13
        else:
            if self.physic_eat is 1:
                result = 6
            else:
                if self.nurse_press is 0:
                    result = 22 if self.physic_control_defecation is not 3 else 23
                else:
                    result = 24 if self.behav_sad is 0 else 25

        return BATH_DIC[result]

    def eat_diagram(self):
        if self.physic_eat is not 3:
            if self.physic_brush_teeth is not 3:
                if self.physic_brush_teeth is 1:
                    result = 11 if self.physic_score <= 6.59 else 12
                else:
                    if self.physic_stand_sit is 1:
                        result = 17 if self.behav_go_outside is 0 else 18
                    else:
                        result = 14
            else:
                if self.physic_use_bathroom is not 3:
                    if self.physic_control_defecation is 1:
                        result = 15
                    else:
                        result = 19 if self.rehab_score <= 30.77 else 20
                else:
                    result = 10
        else:
            result = 5 if self.rehab_score <= 41.21 else 6

        return EAT_DIC[result]

    def assist_diagram(self):
        if self.physic_score <= 47.64:
            if self.physic_score <= 25.14:
                result = 7 if self.physic_score <= 6.59 else 8
            else:
                if self.physic_use_bathroom is 1:
                    if self.physic_brush_teeth is not 3:
                        result = 21 if self.rehab_right_down is 1 else 22
                    else:
                        result = 16
                else:
                    result = 17 if self.behav_bad_behav is 0 else 18
        else:
            if self.physic_brush_teeth is not 3:
                if self.physic_stand_sit is not 3:
                    result = 19 if self.behav_score <= 28.83 else 20
                else:
                    result = 12
            else:
                result = 13 if self.nurse_press is 0 else 14

        return ASSIST_DIC[result]

    def behav_diagram(self):
        if self.behav_score <= 34.69:
            if self.behav_score <= 7.79:
                result = 7 if self.physic_score <= 17.71 else 8
            else:
                result = 9 if self.recog_score <= 60.24 else 10
        else:
            if self.recog_score <= 39.21:
                result = 5
            else:
                if self.behav_go_outside is 0:
                    result = 11
                else:
                    result = 13 if self.physic_wash_face is not 3 else 14

        return BEHAV_DIC[result]

    def support_diagram(self):
        if self.physic_score <= 25.14:
            result = 3 if self.physic_score <= 6.59 else 4

        else:
            if self.behav_go_outside is 0:
                if self.physic_control_fee is 1:
                    result = 7
                else:
                    if self.behav_sad is 0:
                        if self.physic_eat is 1:
                            result = 13
                        else:
                            result = 15 if self.behav_chaos is 0 else 16
                    else:
                        result = 12
            else:
                result = 9 if self.behav_score <= 56 else 10

        return SUPPROT_DIC[result]

    def nurse_diagram(self):
        if self.nurse_press is 0:
            if self.nurse_score is 0:
                if self.behav_chaos is 0:
                    if self.rehab_left_up is 1:
                        result = 14 if self.behav_lost is 0 else 15
                    else:
                        result = 16 if self.physic_brush_teeth is not 3 else 17
                else:
                    result = 9
            elif self.nurse_score <= 19.84:
                result = 4
            else:
                result = 5
        else:
            if self.physic_eat is not 3:
                result = 10 if self.physic_brush_teeth is not 3 else 11
            else:
                result = 7

        return NURSE_DIC[result]

    def rehab_diagram(self):
        if self.rehab_score is 0:
            result = 4 if self.behav_lost is 0 else 5
        elif self.rehab_score <= 39.46:
            if self.physic_wash_face is not 3:
                if self.physic_move_sit is 1:
                    if self.recog_place is 0:
                        result = 16 if self.physic_brush_teeth is 1 else 17
                    else:
                        result = 18 if self.physic_clothes is 1 else 19
                else:
                    result = 11
            else:
                result = 12 if self.physic_stand_sit is not 3 else 13
        else:
            result = 8 if self.behav_sad is 0 else 9

        return REHAB_DIC[result]

    def get_rate(self, score):
        if score >= 95:
            rate = 1
        elif score >= 75:
            rate = 2
        elif score >= 60:
            rate = 3
        elif score >= 51:
            rate = 4
        else:
            rate = 5

        return rate

    def get_score(self):
        score = self.clean_diagram() + self.bath_diagram() + self.eat_diagram() \
                + self.assist_diagram() + self.behav_diagram() + self.support_diagram() \
                + self.nurse_diagram() + self.rehab_diagram()

        if self.recog_demen == 1 and score < 75:
            tmp = ((1.37 * self.recog_date) + (1.20 * self.behav_chaos) + (0.89 * self.behav_lost)
                   + (3.29 * self.behav_go_outside) + (0.51 * self.behav_bad_behav) + (1.54 * self.nurse_press)
                   + (1.94 * self.nurse_fee) + (0.5 * self.rehab_left_up) + (0.89 * self.physic_score)
                   + (0.18 * self.behav_score) - 27.00)

            tmp = math.exp(tmp)
            tmp = (tmp / (1 + tmp))

            if tmp >= 0.5:
                if 60 <= score < 75:
                    score = 75
                elif 51 <= score < 60:
                    score = 60
                else:
                    score = 51

        return round(score, 1)


class SimpleAnalysisDiagram:
    physic_score, recog_score, behav_score, nurse_score, rehab_score = 0, 0, 0, 0, 0
    physic_eat, physic_bath, physic_change, physic_wash = 0, 0, 0, 0
    behav_unstable, behav_chaos, behav_sad, behav_bad = 0, 0, 0, 0
    recog_demen, recog_env, recog_judge = 0, 0, 0
    rehab_right, rehab_left, rehab_low, rehab_up = 0, 0, 0, 0
    nurse_press, nurse_dialy = 0, 0

    def save(self, data):
        global CONVERT_PHYSIC, CONVERT_REHAB, CONVERT_BEHAV, CONVERT_RECOG, CONVERT_NURSE
        physical, recognize, behavior, nursing, rehab = data['physical'], data['recognize'], data['behavior'], data[
            'nursing'], data['rehabilitation']

        # -- 신체기능 설문 점수 저장 --#
        temp = 0
        weight = 12 / 4
        for value in physical.values():
            temp += weight * int(value)

        self.physic_score = CONVERT_PHYSIC[round(temp)]
        self.physic_eat = int(physical["physicalQuestionnaire1"])
        self.physic_bath = int(physical["physicalQuestionnaire2"])
        self.physic_change = int(physical["physicalQuestionnaire3"])
        self.physic_wash = int(physical["physicalQuestionnaire4"])

        # -- 인지기능 설문 점수 저장 --#
        temp = 0
        weight = 7 / 3
        for value in recognize.values():
            temp += weight * int(value)

        self.recog_score = CONVERT_RECOG[round(temp)]
        self.recog_demen = int(recognize["recognizeQuestionnaire1"])
        self.recog_env = int(recognize["recognizeQuestionnaire2"])
        self.recog_judge = int(recognize["recognizeQuestionnaire3"])

        # -- 행동변화 설문 점수 저장 --#
        temp = 0
        weight = 14 / 4
        for value in behavior.values():
            temp += weight * int(value)

        self.behav_score = CONVERT_BEHAV[round(temp)]
        self.behav_unstable = int(behavior["behaviorQuestionnaire1"])
        self.behav_chaos = int(behavior["behaviorQuestionnaire2"])
        self.behav_sad = int(behavior["behaviorQuestionnaire3"])
        self.behav_bad = int(behavior["behaviorQuestionnaire4"])

        # -- 간호처치 설문 점수 저장 --#
        temp = 0
        weight = 9 / 2
        for value in nursing.values():
            temp += weight * int(value)

        self.nurse_score = CONVERT_NURSE[round(temp)]
        self.nurse_press = int(nursing["nursingQuestionnaire1"])
        self.nurse_dialy = int(nursing["nursingQuestionnaire2"])

        # -- 재활영역 설문 점수 저장 --#
        temp = 0
        weight = 10 / 4
        for value in rehab.values():
            temp += weight * int(value)

        self.rehab_score = CONVERT_REHAB[round(temp)]
        self.rehab_right = int(rehab["rehabilitationQuestionnaire1"])
        self.rehab_left = int(rehab["rehabilitationQuestionnaire2"])
        self.rehab_low = int(rehab["rehabilitationQuestionnaire3"])
        self.rehab_up = int(rehab["rehabilitationQuestionnaire4"])

    # == 청결 수형분석도 ==#
    def clean_diagram(self):
        if self.physic_score <= 34.15:
            if self.physic_score <= 17.72:
                if self.recog_score <= 9.86:
                    result = 15 if self.physic_score <= 6.59 else 16
                else:
                    result = 17 if self.recog_score <= 39.21 else 18
            else:
                result = 9 if self.recog_env == 0 else 10
        else:
            if self.physic_wash != 3:
                if self.physic_bath == 1:
                    result = 11
                else:
                    result = 19 if self.recog_env == 0 else 20
            else:
                if self.physic_bath == 1:
                    result = 13
                else:
                    if self.rehab_score <= 40.16:
                        result = 23 if self.behav_score <= 60.34 else 24
                    else:
                        result = 22

        return CLEAN_DIC[result]

    # == 배설 수형분석도 ==#
    def bath_diagram(self):
        if self.physic_change == 1:
            if self.physic_bath is 1:
                if self.physic_change is 1:
                    if self.physic_score is 0:
                        if self.recog_judge is 0:
                            result = 30 if self.behav_score <= 15.58 else 31
                        else:
                            result = 27
                    else:
                        if self.rehab_low is 1:
                            result = 28
                        else:
                            result = 32 if self.recog_env is 0 else 33
                else:
                    result = 9
            elif self.physic_bath is 2:
                if self.physic_change is 1:
                    result = 18 if self.physic_bath is 1 else 19
                else:
                    result = 11
            else:
                if self.behav_unstable is 0:
                    result = 20 if self.physic_wash is 1 else 21
                else:
                    result = 13
        else:
            if self.physic_eat is 1:
                result = 6
            else:
                if self.nurse_press is 0:
                    result = 22 if self.physic_bath is not 3 else 23
                else:
                    result = 24 if self.behav_sad is 0 else 25

        return BATH_DIC[result]

    # == 식사 수형분석도 ==#
    def eat_diagram(self):
        if self.physic_eat is not 3:
            if self.physic_wash is not 1:
                if self.physic_wash is 1:
                    result = 11 if self.physic_score <= 6.59 else 12
                else:
                    if self.physic_change is 1:
                        result = 17 if self.behav_unstable is 0 else 18
                    else:
                        result = 14
            else:
                if self.physic_bath is not 3:
                    result = 19 if self.rehab_score <= 30.77 else 20
                else:
                    result = 10
        else:
            result = 5 if self.rehab_score <= 41.21 else 6

        return EAT_DIC[result]

    # == 기능보조 수형분석도 ==#
    def assist_diagram(self):
        if self.physic_score <= 47.64:
            if self.physic_score <= 25.14:
                result = 7 if self.physic_score <= 6.59 else 8
            else:
                if self.physic_bath is 1:
                    if self.physic_wash is not 3:
                        result = 21 if self.rehab_right is 1 else 22
                    else:
                        result = 16
                else:
                    result = 17 if self.behav_bad is 0 else 18
        else:
            if self.physic_wash is not 3:
                if self.physic_change is not 3:
                    result = 19 if self.behav_score <= 28.83 else 20
                else:
                    result = 12
            else:
                result = 13 if self.nurse_press is 0 else 14

        return ASSIST_DIC[result]

    # == 행동변화대응 수형분석도 ==#
    def behav_diagram(self):
        if self.behav_score <= 34.69:
            if self.behav_score <= 7.79:
                result = 7 if self.physic_score <= 17.71 else 8
            else:
                result = 9 if self.recog_score <= 60.24 else 10
        else:
            if self.recog_score <= 39.21:
                result = 5
            else:
                if self.behav_unstable is 0:
                    result = 11
                else:
                    result = 13 if self.physic_wash is not 3 else 14

        return BEHAV_DIC[result]

    # == 간접지원 수형분석도 ==#
    def support_diagram(self):
        if self.physic_score <= 25.14:
            result = 3 if self.physic_score <= 6.59 else 4
        else:
            if self.behav_unstable is 0:
                if self.physic_bath is 1:
                    result = 7
                else:
                    if self.behav_sad is 0:
                        if self.physic_eat is 1:
                            result = 13
                        else:
                            result = 15 if self.behav_chaos is 0 else 16
                    else:
                        result = 12
            else:
                result = 9 if self.behav_score <= 56 else 10

        return SUPPROT_DIC[result]

    # == 간호처치 수형분석도 ==#
    def nurse_diagram(self):
        if self.nurse_press is 0:
            if self.nurse_score is 0:
                if self.behav_chaos is 0:
                    if self.rehab_left is 1:
                        result = 14 if self.behav_unstable is 0 else 15
                    else:
                        result = 16 if self.physic_wash is not 3 else 17
                else:
                    result = 9
            elif self.nurse_score <= 19.84:
                result = 4
            else:
                result = 5
        else:
            if self.physic_eat is not 3:
                result = 10 if self.physic_wash is not 3 else 11
            else:
                result = 7

        return NURSE_DIC[result]

    # == 재활훈련 수형분석도 ==#
    def rehab_diagram(self):
        if self.rehab_score is 0:
            result = 4 if self.behav_unstable is 0 else 5
        elif self.rehab_score <= 39.46:
            if self.physic_wash is not 3:
                if self.physic_change is 1:
                    if self.recog_env is 0:
                        result = 16 if self.physic_wash is 1 else 17
                    else:
                        result = 18 if self.physic_change is 1 else 19
                else:
                    result = 11
            else:
                result = 12 if self.physic_change is not 3 else 13
        else:
            result = 8 if self.behav_sad is 0 else 9

        return REHAB_DIC[result]

    # == 등급평가 ==#
    def get_rate(self, score):
        if score >= 95:
            rate = 1

        elif score >= 75:
            rate = 2

        elif score >= 60:
            rate = 3

        elif score >= 51:
            rate = 4

        else:
            rate = 5

        return rate

    def get_score(self):
        score = self.clean_diagram() + self.bath_diagram() + self.eat_diagram() \
                + self.assist_diagram() + self.behav_diagram() + self.support_diagram() \
                + self.nurse_diagram() + self.rehab_diagram()

        return round(score, 1)
