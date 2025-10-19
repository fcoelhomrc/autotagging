from data.scraping import query, process_response

def main():
    response = query("leather jacket")
    process_response(response)

if __name__ == "__main__":
    main()