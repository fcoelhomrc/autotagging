from data.scraping import query, process_response


def main():
    search_text = "leather jacket"
    response = query(search_text)
    process_response(response, search_text)


if __name__ == "__main__":
    main()
