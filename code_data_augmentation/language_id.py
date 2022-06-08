import fasttext  # pip install fasttext-wheel
import logging
from typing import Dict
from pathlib import Path


def get_langid(txt: str = '') -> Dict:
    # get language predictions for a given string

    # return a dict
    # lang_dict: { 'lang_id': <string>,
    #              'lang_id_confidence' : <number>,
    #              'lang_id_predictions': <string>

    lang_dict = {}
    lang_dict['lang_id'] = ''
    lang_dict['lang_id_confidence'] = 0
    lang_dict['lang_id_predictions'] = ''

    lang_id_model_path = '../lid.176.bin'
    if Path(lang_id_model_path).exists():
        lang_id_model = fasttext.load_model(lang_id_model_path)
    else:
        logging.error(f'FastTest language model file not found: {lang_id_model_path}')
        return lang_dict

    if type(txt) != str:
        logging.warning(f'Input: not_string; type: {type(txt)}')
        return lang_dict
    if len(txt) < 5:
        logging.warning(f'Input: {txt}; Input too short')
        return lang_dict

    sent_list = [txt]
    predictions = None

    try:
        predictions = lang_id_model.predict(sent_list, k=3)
    except Exception as err:
        logging.error(str(err))

    if predictions:
        # logging.info(f'Input: "{sent_list[0]:.60}" Prediction: {prediction}')  # log only the first few characters of the string
        # lang_prediction = prediction[0][0][0].replace('__label__', '')
        multi_predictions = zip([label.replace('__label__', '') for label in predictions[0][0]], [confidence for confidence in predictions[1][0]])
        multi_predictions_str = ', '.join([f'{lang}={conf:.4f}' for lang, conf in list(multi_predictions)])
        lang_id = predictions[0][0][0].replace('__label__', '')
        lang_id_confidence = predictions[1][0][0]

        lang_dict['lang_id'] = lang_id
        lang_dict['lang_id_confidence'] = float(f'{lang_id_confidence:.4f}')
        lang_dict['lang_id_predictions'] = multi_predictions_str

    return lang_dict


if __name__ == '__main__':
    input_str = 'These findings have positive implications regarding vaccination efficacy in this group.'

    print(get_langid(input_str))
    # {'lang_id': 'en', 'lang_id_confidence': 0.9082, 'lang_id_predictions': 'en=0.9082, zh=0.0078, de=0.0075'}
