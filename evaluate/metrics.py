import json

class Charades_Test:
    def __init__(self, annotation_file, pred_file):
        self.data = {}
        self.load_annotations(annotation_file)
        self.load_pred(pred_file)

    def load_annotations(self, json_file):
        with open(json_file, 'r') as file:
            json_data = json.load(file)
            for entry in json_data:
                self.data[entry['id']] = {
                    'video': entry['video'],
                    'start_time': entry['start_time'],
                    'end_time': entry['end_time'],
                    'query': entry['query']
                }
    def load_pred(self, json_file):
        with open(json_file, 'r') as file:
            json_data = json.load(file)
            for entry in json_data:
                self.data[entry['id']]['start_frame'] = entry['start_frame']
                self.data[entry['id']]['end_frame'] = entry['end_frame']
    def get_len(self):
        return len(self.data)
    
    def calculate_tIoU(self, gt_start, gt_end, pred_start, pred_end):
        intersection_start = max(gt_start, pred_start)
        intersection_end = min(gt_end, pred_end)
        intersection = max(0, intersection_end - intersection_start)
        union = (gt_end - gt_start) + (pred_end - pred_start) - intersection
        tIoU = intersection / union if union != 0 else 0
        return tIoU

    def calculate_all_tIoUs(self):
        results = {}
        for entry_id, entry in self.data.items():
            gt_start = entry['start_time']
            gt_end = entry['end_time']
            pred_start = entry.get('start_frame', None)
            pred_end = entry.get('end_frame', None)
            
            if pred_start is not None and pred_end is not None:
                tIoU = self.calculate_tIoU(gt_start, gt_end, pred_start, pred_end)
                results[entry_id] = tIoU
            else:
                results[entry_id] = None  # No prediction available
        
        return results

    def calculate_recall_at_tIoU(self, tIoU_threshold):
        tIoU_results = self.calculate_all_tIoUs()
        correct_predictions = 0
        total_predictions = 0
        
        for tIoU in tIoU_results.values():
            if tIoU is not None:
                total_predictions += 1
                if tIoU >= tIoU_threshold:
                    correct_predictions += 1
        
        recall = correct_predictions / total_predictions if total_predictions > 0 else 0
        return recall

    def calculate_recall_at_multiple_tIoUs(self, thresholds=[0.3, 0.5, 0.7]):
        recalls = {}
        for threshold in thresholds:
            recalls[f'R@1 (IoU={threshold})'] = self.calculate_recall_at_tIoU(threshold)
        return recalls

    def calculate_mIoU(self):
        tIoU_results = self.calculate_all_tIoUs()
        total_tIoU = 0
        count = 0

        for tIoU in tIoU_results.values():
            if tIoU is not None:
                total_tIoU += tIoU
                count += 1

        mIoU = total_tIoU / count if count > 0 else 0
        return mIoU

    def evaluate(self):
        recalls = self.calculate_recall_at_multiple_tIoUs()
        mIoU = self.calculate_mIoU()
        recalls['mIoU'] = mIoU
        return recalls
        
charades_test = Charades_Test('evaluate/charades_sta_test.json','results/pred.json')
recalls = charades_test.evaluate()
