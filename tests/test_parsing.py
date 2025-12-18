from Core.parse import parse_pipeline


def test_valid_number():
    result = parse_pipeline("9058578790", region="IN")
    assert result["success"] is True


def test_invalid_number():
    result = parse_pipeline("123", region="IN")
    assert result["success"] is False


if __name__ == "__main__":
    test_valid_number()
    test_invalid_number()
    print("Parsing tests passed")
