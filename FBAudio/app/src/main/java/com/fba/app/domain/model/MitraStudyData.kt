package com.fba.app.domain.model

data class MitraModule(
    val id: String,
    val name: String,
    val year: Int,
    val talks: List<MitraTalk>,
    val seriesCodes: List<String> = emptyList(),
)

data class MitraTalk(
    val catNum: String,
    val title: String,
    val speaker: String,
    val imageUrl: String = "",
)

object MitraStudyData {

    val modules: List<MitraModule> = listOf(
        // ── Year 1 ──────────────────────────────────────────────────
        MitraModule(
            id = "y1_refuge", name = "Going for Refuge", year = 1,
            seriesCodes = listOf("X04"),
            talks = listOf(
                MitraTalk("09", "Going for Refuge", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("137", "Levels of Going for Refuge", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("154", "Dimensions of Going for Refuge", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("171", "The History of My Going for Refuge", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("08", "Introducing Buddhism", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("19", "The Approach to Buddhism", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("139", "The Taste of Freedom", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
            ),
        ),
        MitraModule(
            id = "y1_ethics", name = "Ethics", year = 1,
            talks = listOf(
                MitraTalk("161", "The Ten Pillars of Buddhism", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("LOC3546", "The Ten Pillars of Buddhism Part 1", "Padmavajra", "https://www.freebuddhistaudio.com/m/74F3308hMMvn.jpg"),
            ),
        ),
        MitraModule(
            id = "y1_meditation", name = "Meditation", year = 1,
            talks = listOf(
                MitraTalk("135", "A System of Meditation", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
            ),
        ),
        MitraModule(
            id = "y1_wisdom", name = "Wisdom", year = 1,
            talks = listOf(
                MitraTalk("24", "The Dynamics of Being", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("31", "Mind: Reactive and Creative", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("103", "The Symbolism of the Tibetan Wheel of Life", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
            ),
        ),
        MitraModule(
            id = "y1_triratna", name = "Buddhism and Triratna", year = 1,
            talks = listOf(
                MitraTalk("LOC517", "Triratna Buddhism", "Vadanya", "https://www.freebuddhistaudio.com/images/people/vadanya.jpg"),
                MitraTalk("36", "The Psychology of Buddhist Ritual", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
            ),
        ),

        // ── Year 2 ──────────────────────────────────────────────────
        MitraModule(
            id = "y2_eightfold", name = "Noble Eightfold Path", year = 2,
            seriesCodes = listOf("X07"),
            talks = listOf(
                MitraTalk("47", "The Nature of Existence: Right Understanding", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("48", "Reason and Emotion in the Spiritual Life: Right Resolve", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("49", "The Ideal of Human Communication: Right Speech", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("50", "The Principles of Ethics: Right Action", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("51", "The Ideal Society: Right Livelihood", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("52", "The Conscious Evolution of Man: Right Effort", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("53", "Levels of Awareness: Right Mindfulness", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("54", "Samadhi, the Higher Consciousness: Right Meditation", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("185", "The Transcendental Eightfold Path", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
            ),
        ),
        MitraModule(
            id = "y2_conditionality", name = "Pratitya-Samutpada", year = 2,
            talks = listOf(
                MitraTalk("24", "The Dynamics of Being", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("LOC432", "Revering and Relying Upon the Dharma", "Subhuti", "https://www.freebuddhistaudio.com/m/OKSt7sgcGxBe.jpg"),
                MitraTalk("LOC217", "Twenty Four Nidana Reflection", "Dhivan", "https://www.freebuddhistaudio.com/m/fVZq9magtguB.jpg"),
            ),
        ),
        MitraModule(
            id = "y2_five_aspects", name = "Five Aspects of Dharma Life", year = 2,
            seriesCodes = listOf("X74"),
            talks = listOf(
                MitraTalk("LOC1691", "The Five Aspects of Dharma Life - Integration", "Subhuti", "https://www.freebuddhistaudio.com/m/OKSt7sgcGxBe.jpg"),
                MitraTalk("LOC1698", "The Five Aspects of Dharma Life - Positive Emotion", "Subhuti", "https://www.freebuddhistaudio.com/m/OKSt7sgcGxBe.jpg"),
                MitraTalk("LOC1699", "The Five Aspects of Dharma Life - Questions and Answers", "Subhuti", "https://www.freebuddhistaudio.com/m/OKSt7sgcGxBe.jpg"),
                MitraTalk("LOC1701", "The Five Aspects of Dharma Life - Spiritual Receptivity", "Subhuti", "https://www.freebuddhistaudio.com/m/OKSt7sgcGxBe.jpg"),
                MitraTalk("LOC1714", "The Five Aspects of Dharma Life - Spiritual Rebirth", "Subhuti", "https://www.freebuddhistaudio.com/m/OKSt7sgcGxBe.jpg"),
                MitraTalk("LOC1715", "The Five Aspects of Dharma Life - Applying the Five Aspects in Daily Life", "Subhuti", "https://www.freebuddhistaudio.com/m/OKSt7sgcGxBe.jpg"),
            ),
        ),
        MitraModule(
            id = "y2_mind_turning", name = "Turning the Mind", year = 2,
            seriesCodes = listOf("X25"),
            talks = listOf(
                MitraTalk("OM739", "The Four Mind-Turning Reflections", "Dhammadinna", "https://www.freebuddhistaudio.com/m/EjVD2wfyd4Af.jpg"),
                MitraTalk("OM743", "The Defects and Dangers of Samsara", "Maitreyi", "https://www.freebuddhistaudio.com/images/people/maitreyi.jpg"),
                MitraTalk("LOC51", "Maturing the Mind - Introduction to the Four Reminders", "Kulaprabha", "https://www.freebuddhistaudio.com/images/people/kulaprabha.jpg"),
            ),
        ),
        MitraModule(
            id = "y2_mindfulness", name = "Way of Mindfulness", year = 2,
            seriesCodes = listOf("X93"),
            talks = listOf(
                MitraTalk("OM838", "The Way of Mindfulness - Introduction to the Satipatthana Sutta", "Vidyamala", "https://www.freebuddhistaudio.com/images/people/vidyamala.jpg"),
                MitraTalk("M14", "The Way of Mindfulness Week 1 - Awareness Meditation", "Vidyamala", "https://www.freebuddhistaudio.com/images/people/vidyamala.jpg"),
                MitraTalk("M15", "The Way of Mindfulness Week 2 - Body Scan (Breath-Based)", "Vidyamala", "https://www.freebuddhistaudio.com/images/people/vidyamala.jpg"),
                MitraTalk("M16", "The Way of Mindfulness Week 3 - Vedana Meditation", "Vidyamala", "https://www.freebuddhistaudio.com/images/people/vidyamala.jpg"),
                MitraTalk("M17", "The Way of Mindfulness Week 4 - Unworldly Vedana Meditation", "Vidyamala", "https://www.freebuddhistaudio.com/images/people/vidyamala.jpg"),
                MitraTalk("M18", "The Way of Mindfulness Week 5 - Citta Meditation", "Vidyamala", "https://www.freebuddhistaudio.com/images/people/vidyamala.jpg"),
                MitraTalk("M19", "The Way of Mindfulness Week 6 - Working with Thoughts and Emotions", "Vidyamala", "https://www.freebuddhistaudio.com/images/people/vidyamala.jpg"),
                MitraTalk("M20", "The Way of Mindfulness Week 7 - Hindrances and Awakening Factors", "Vidyamala", "https://www.freebuddhistaudio.com/images/people/vidyamala.jpg"),
                MitraTalk("LOC1016", "Living with Awareness (A Guide to the Satipatthana Sutta) - Part 1", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("LOC1017", "Living with Awareness (A Guide to the Satipatthana Sutta) - Part 2", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("LOC1018", "Living with Awareness (A Guide to the Satipatthana Sutta) - Part 4", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
            ),
        ),
        MitraModule(
            id = "y2_sangha", name = "What is the Sangha?", year = 2,
            talks = listOf(
                MitraTalk("142", "Commitment and Spiritual Community", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("LOC2121", "Year of Spiritual Community Talks", "Various", "https://www.freebuddhistaudio.com/images/people/various.jpg"),
            ),
        ),
        MitraModule(
            id = "y2_tradition", name = "A Living Tradition", year = 2,
            seriesCodes = listOf("X100"),
            talks = listOf(
                MitraTalk("LOC517", "Triratna Buddhism", "Vadanya", "https://www.freebuddhistaudio.com/images/people/vadanya.jpg"),
            ),
        ),

        // ── Year 3 ──────────────────────────────────────────────────
        MitraModule(
            id = "y3_pali", name = "Selected Suttas (Pali Canon)", year = 3,
            talks = listOf(
                MitraTalk("S01", "Readings from the Pali Canon", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("LOC45", "The Early Teachings of the Buddha", "Ratnaguna", "https://www.freebuddhistaudio.com/m/4KlYlo7LoMfB.jpg"),
            ),
        ),
        MitraModule(
            id = "y3_dhammapada", name = "The Dhammapada", year = 3,
            seriesCodes = listOf("X37"),
            talks = listOf(
                MitraTalk("OM790", "The Essential Revolution - Dhammapada Verses 1 & 2", "Padmavajra", "https://www.freebuddhistaudio.com/m/74F3308hMMvn.jpg"),
                MitraTalk("OM791", "Changing Hatred into Love - Dhammapada Verses 3 to 6", "Padmavajra", "https://www.freebuddhistaudio.com/m/74F3308hMMvn.jpg"),
                MitraTalk("OM792", "Mindfulness is the Way to the Deathless - Dhammapada Verses 7, 8, 21 & 23", "Padmavajra", "https://www.freebuddhistaudio.com/m/74F3308hMMvn.jpg"),
                MitraTalk("OM793", "Seeing with Insight - Dhammapada Verses 277 to 279", "Padmavajra", "https://www.freebuddhistaudio.com/m/74F3308hMMvn.jpg"),
                MitraTalk("OM794", "Flowers - Dhammapada Verses 44 to 59", "Padmavajra", "https://www.freebuddhistaudio.com/m/74F3308hMMvn.jpg"),
            ),
        ),
        MitraModule(
            id = "y3_insight", name = "Towards Insight", year = 3,
            talks = listOf(
                MitraTalk("LOC100", "Towards Insight - Contemplations of the Buddha", "Dayanandi and Ratnaguna", "https://www.freebuddhistaudio.com/images/talks/LOC100.jpg"),
                MitraTalk("LOC101", "Towards Insight - Contemplation of Impermanence", "Dayanandi and Ratnaguna", "https://www.freebuddhistaudio.com/images/talks/LOC101.jpg"),
            ),
        ),
        MitraModule(
            id = "y3_mahayana", name = "Mahayana Perspectives", year = 3,
            talks = listOf(
                MitraTalk("143", "The Magic of a Mahayana Sutra", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
            ),
        ),

        // ── Year 4 ──────────────────────────────────────────────────
        MitraModule(
            id = "y4_bodhisattva", name = "The Bodhisattva Ideal", year = 4,
            seriesCodes = listOf("X09"),
            talks = listOf(
                MitraTalk("65", "The Origin and Development of the Bodhisattva Ideal", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("67", "The Bodhisattva Vow", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("71", "The Bodhisattva Hierarchy", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("LOC1020", "The Bodhisattva Ideal: Wisdom and Compassion in Buddhism - Part 1", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("LOC3419", "The Bodhisattva Ideal - Talk 6", "Subhuti", "https://www.freebuddhistaudio.com/m/OKSt7sgcGxBe.jpg"),
            ),
        ),
        MitraModule(
            id = "y4_sangha", name = "Nature of the Sangha", year = 4,
            talks = listOf(
                MitraTalk("142", "Commitment and Spiritual Community", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
            ),
        ),
        MitraModule(
            id = "y4_symbols", name = "Faith, Symbols, and Imagination", year = 4,
            seriesCodes = listOf("X13"),
            talks = listOf(
                MitraTalk("103", "The Symbolism of the Tibetan Wheel of Life", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("104", "The Tantric Symbolism of the Stupa", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("45", "The Mandala: Tantric Symbol of Integration", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
            ),
        ),
        MitraModule(
            id = "y4_ethics_env", name = "Ethics and Environment", year = 4,
            seriesCodes = listOf("X141"),
            talks = listOf(
                MitraTalk("LOC3566", "Introducing Ethics: Resonating with Reality", "Maitrisiddhi", "https://www.freebuddhistaudio.com/m/t3k3UrtQ0pxL.jpg"),
                MitraTalk("LOC3565", "Metta Versus Pema: Love and Attachment", "Dharmakarunya", "https://www.freebuddhistaudio.com/images/people/dharmakarunya.jpg"),
                MitraTalk("LOC3563", "Love and Sex - The Third Precept", "Sahajatara", "https://www.freebuddhistaudio.com/images/people/sahajatara.jpg"),
                MitraTalk("LOC3564", "The Speech Precepts", "Sahajatara", "https://www.freebuddhistaudio.com/images/people/sahajatara.jpg"),
                MitraTalk("LOC3567", "The Ethics of Mindfulness", "Maitrisiddhi", "https://www.freebuddhistaudio.com/m/t3k3UrtQ0pxL.jpg"),
            ),
        ),
        MitraModule(
            id = "y4_psychology", name = "Buddhist Psychology", year = 4,
            talks = listOf(
                MitraTalk("40", "The Analytical Psychology of the Abhidharma", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("41", "The Psychology of Spiritual Development", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
                MitraTalk("31", "Mind: Reactive and Creative", "Sangharakshita", "https://www.freebuddhistaudio.com/m/uKp8bNgbigXw.jpg"),
            ),
        ),
        MitraModule(
            id = "y4_history", name = "History of Triratna", year = 4,
            seriesCodes = listOf("X100"),
            talks = listOf(
                MitraTalk("LOC517", "Triratna Buddhism", "Vadanya", "https://www.freebuddhistaudio.com/images/people/vadanya.jpg"),
            ),
        ),
    )

    /** Get modules grouped by year. */
    fun modulesByYear(): Map<Int, List<MitraModule>> = modules.groupBy { it.year }

    /** Convert module talks to SearchResult list for display in browse screen. */
    fun moduleTalksAsSearchResults(moduleId: String): List<SearchResult> {
        val module = modules.find { it.id == moduleId } ?: return emptyList()
        return module.talks.map { talk ->
            SearchResult(
                catNum = talk.catNum,
                title = talk.title,
                speaker = talk.speaker,
                imageUrl = talk.imageUrl,
                path = "https://www.freebuddhistaudio.com/audio/details?num=${talk.catNum}",
            )
        }
    }

    /** Get year sub-categories as BrowseCategory list. */
    fun yearCategories(): List<BrowseCategory> {
        return (1..4).map { year ->
            BrowseCategory(
                id = "mitra_year_$year",
                name = "Year $year",
                type = CategoryType.MITRA_YEAR,
                browseUrl = "mitra://year/$year",
            )
        }
    }

    /** Get module sub-categories for a given year. */
    fun moduleCategories(year: Int): List<BrowseCategory> {
        return modules.filter { it.year == year }.map { module ->
            BrowseCategory(
                id = module.id,
                name = module.name,
                type = CategoryType.MITRA_MODULE,
                browseUrl = "mitra://module/${module.id}",
            )
        }
    }
}
