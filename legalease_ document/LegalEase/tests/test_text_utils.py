from backend.utils.text_utils import clean_text, make_title, word_count


def test_clean_text():
    assert clean_text(" hello \r\n\r\n\r\nworld ") == "hello\n\nworld"


def test_make_title():
    assert make_title("Affidavit") == "Affidavit"


def test_word_count():
    assert word_count("Hello legal world") == 3
