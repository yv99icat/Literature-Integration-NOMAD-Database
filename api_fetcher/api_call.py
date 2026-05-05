from tools import post_data, save_json
from project_variable import variables


def fetch_solar_cell_references():
    references = []
    counter = 0
    page_value = None

    while True:
        # Define request payload
        data = {
            "owner": "visible",
            "query": {
                "and": [{}, {"sections:all": ["nomad.datamodel.results.SolarCell"]}]
            },
            "aggregations": {},
            "pagination": {
                "order_by": "results.properties.optoelectronic.solar_cell.efficiency",
                "page_after_value": page_value,
                "order": "desc",
                "page_size": 1000
            },
            "required": {
                "exclude": ["quantities", "sections", "files"]
            }
        }

        # Make API request
        response = post_data(variables["POST_META_DATA"], data)

        # Check for pagination termination
        next_page = response["pagination"].get("next_page_after_value")
        if not next_page:
            print("No more pages, data is finished.")
            break

        # Update counter and page_value for next request
        counter += 1
        page_value = next_page

        # Process the references
        meta_data = response.get("data", [])
        for item in meta_data:
            # Append first reference if available
            if item.get("references"):
                references.append(item["references"][0])

        print(f"Page {counter} processed, next page: {next_page}")

    # Save the collected references to a file
    save_json(references, "doi_solar_cell.json")
    print(f"Total pages processed: {counter}")


if __name__ == "__main__":
    fetch_solar_cell_references()
