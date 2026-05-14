class Validator:
    def validateFormat(self, data):
        # 3. (received) SubmissionController -> Validator : validateFormat(data)
        # 4. (return) Validator --> SubmissionController : valid/invalid
        if not data:
            return "invalid"
        required_fields = ["title", "content", "author_id"]
        for field in required_fields:
            if field not in data or not data[field]:
                return "invalid"
        return "valid"
