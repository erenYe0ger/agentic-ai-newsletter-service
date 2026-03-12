def select_final_articles(articles: list[dict[str, str]]) -> list[dict[str, str]]:

    deepmind_article = None
    hf_article = None
    others = []

    for article in articles:

        link = article["link"]

        if not deepmind_article and "deepmind.google" in link:
            deepmind_article = article

        elif not hf_article and "huggingface.co" in link:
            hf_article = article

        else:
            others.append(article)

    final_articles = []

    if deepmind_article:
        final_articles.append(deepmind_article)

    if hf_article:
        final_articles.append(hf_article)

    for article in others:
        if len(final_articles) >= 5:
            break
        final_articles.append(article)

    return final_articles