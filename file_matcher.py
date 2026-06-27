
class MappingNotFoundError(Exception):
    pass

class MultipleMappingsFoundError(Exception):
    pass

def get_mapping_for_file(filename: str,mappings: dict):
    filename = filename.upper()

    matches = []

    for pattern,mapping in mappings.items():

        if pattern.upper() in filename:
            matches.append((pattern,mapping))

    if not matches:
        raise MappingNotFoundError(
            f"No mapping found for file: {filename}"
        )
    if len(matches)>1 :
        matched_patterns = [pattern for pattern,_ in matches]

        raise MultipleMappingsFoundError(
            f"Multiple mappings found for {filename}: "
            f"{matched_patterns}"
        )
    return matches[0]