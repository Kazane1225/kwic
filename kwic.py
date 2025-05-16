from collections import Counter

def colorize(text, color="red", attrs=["bold"]):
    styles = []
    if "bold" in attrs:
        styles.append("font-weight:bold")
    if "underline" in attrs:
        styles.append("text-decoration:underline")
    style_str = f"color:{color};" + ";".join(styles)
    return f'<span style="{style_str}">{text}</span>'

def kwic_search(doc, search_type, query, window=5, color='red', attrs=['bold'], sort_mode='sequential'):
    tokens = list(doc)
    results_with_metadata = []

    if search_type == "entity":
        for ent in doc.ents:
            if ent.label_ == query:
                start, end = ent.start, ent.end
                left = tokens[max(0, start - window):start]
                right = tokens[end:end + window]
                target = colorize(" ".join(t.text for t in tokens[start:end]), color, attrs)
                result = f"... {' '.join(t.text for t in left)} {target} {' '.join(t.text for t in right)} ..."
                results_with_metadata.append((result, right[0].text if right else None, right[0].pos_ if right else None))
    else:
        for i in range(len(tokens)):
            match = False
            if search_type == "token" and tokens[i].text.lower() == query.lower():
                match = True
            elif search_type == "pos" and tokens[i].pos_ == query:
                match = True
            elif search_type == "ngram":
                query_tokens = query.split()
                span = tokens[i:i+len(query_tokens)]
                if len(span) == len(query_tokens) and all(span[j].text.lower() == query_tokens[j].lower() for j in range(len(query_tokens))):
                    match = True
            if match:
                start = i
                end = i + (len(query.split()) if search_type == "ngram" else 1)
                left = tokens[max(0, start - window):start]
                right = tokens[end:end + window]
                if search_type == "ngram":
                    target = " ".join(colorize(t.text, color, attrs) for t in tokens[start:end])
                else:
                    target = colorize(tokens[i].text, color, attrs)
                result = f"... {' '.join(t.text for t in left)} {target} {' '.join(t.text for t in right)} ..."
                results_with_metadata.append((result, right[0].text if right else None, right[0].pos_ if right else None))

    # ソート
    if sort_mode == 'token':
        freq = Counter([m[1] for m in results_with_metadata if m[1]])
        results_with_metadata.sort(key=lambda x: (-freq.get(x[1], 0), x[1]))
    elif sort_mode == 'pos':
        freq = Counter([m[2] for m in results_with_metadata if m[2]])
        results_with_metadata.sort(key=lambda x: (-freq.get(x[2], 0), x[2]))

    return results_with_metadata
