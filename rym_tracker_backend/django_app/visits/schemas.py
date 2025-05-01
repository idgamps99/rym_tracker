RECORD_VISIT_SCHEMA = {
    "type": "object",
    "required": ["isUnique"],
    "properties": {
        "isUnique": {
            "type": "boolean",
            "description": "Whether this visit is unique"
        }
    },
    "additionalProperties": False
}
