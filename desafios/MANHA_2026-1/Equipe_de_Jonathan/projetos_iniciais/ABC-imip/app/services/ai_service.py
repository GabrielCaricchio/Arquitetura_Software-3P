def generate_feedback(score, total_questions):

    percentage = (score / total_questions) * 100

    if percentage >= 80:
        return (
            "A criança apresentou ótimo desempenho "
            "e boa compreensão das palavras."
        )

    elif percentage >= 50:
        return (
            "A criança demonstrou progresso, "
            "mas ainda possui dificuldades."
        )

    else:
        return (
            "A criança precisa de maior reforço "
            "nas atividades de alfabetização."
        )