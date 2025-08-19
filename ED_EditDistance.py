def levenshtein_distance(word_a, word_b):
    len_a = len(word_a)
    len_b = len(word_b)

    # Initialize DP table and operation tracker
    dp = [[0] * (len_b + 1) for _ in range(len_a + 1)]
    op = [[None] * (len_b + 1) for _ in range(len_a + 1)]

    # Fill base cases
    for i in range(len_a + 1):
        dp[i][0] = i
        op[i][0] = 'D'  # Deletion
    for j in range(len_b + 1):
        dp[0][j] = j
        op[0][j] = 'I'  # Insertion

    op[0][0] = None  # No operation at start

    # Fill DP table
    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            if word_a[i - 1] == word_b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                op[i][j] = 'M'  # Match
            else:
                # Compute costs for all operations
                ins = dp[i][j - 1] + 1
                delete = dp[i - 1][j] + 1
                sub = dp[i - 1][j - 1] + 1

                # Choose min and record operation
                dp[i][j] = min(ins, delete, sub)
                if dp[i][j] == sub:
                    op[i][j] = 'S'  # Substitute
                elif dp[i][j] == ins:
                    op[i][j] = 'I'  # Insert
                else:
                    op[i][j] = 'D'  # Delete

    # Trace back for optimal operations
    i, j = len_a, len_b
    operations = []
    aligned_a, aligned_b = "", ""

    num_insert, num_delete, num_sub, num_match = 0, 0, 0, 0

    while i > 0 or j > 0:
        action = op[i][j]
        if action == 'M' or action == 'S':
            a_char = word_a[i - 1]
            b_char = word_b[j - 1]
            aligned_a = a_char + aligned_a
            aligned_b = b_char + aligned_b
            if action == 'M':
                operations.append(f"MATCH     : {a_char} == {b_char}")
                num_match += 1
            else:
                operations.append(f"SUBSTITUTE: {a_char} -> {b_char}")
                num_sub += 1
            i -= 1
            j -= 1
        elif action == 'I':
            a_char = "-"
            b_char = word_b[j - 1]
            aligned_a = a_char + aligned_a
            aligned_b = b_char + aligned_b
            operations.append(f"INSERT    : - -> {b_char}")
            num_insert += 1
            j -= 1
        elif action == 'D':
            a_char = word_a[i - 1]
            b_char = "-"
            aligned_a = a_char + aligned_a
            aligned_b = b_char + aligned_b
            operations.append(f"DELETE    : {a_char} -> -")
            num_delete += 1
            i -= 1

    # Output results
    print("Operations (from last to first):")
    for op_str in reversed(operations):
        print(op_str)

    print("\nAligned Words:")
    print("Word A:", aligned_a)
    print("Word B:", aligned_b)

    print("\nReport:")
    print("Total Minimum Edit Distance :", dp[len_a][len_b])
    print("Number of Insertions        :", num_insert)
    print("Number of Deletions         :", num_delete)
    print("Number of Substitutions     :", num_sub)
    print("Number of Matches           :", num_match)

    return dp[len_a][len_b]

# Example usage
word_a = "characterization"
word_b = "categorization"
levenshtein_distance(word_a, word_b)
