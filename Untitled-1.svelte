<script>
    let traders = [
        {
            id: 1,
            name: "Trader 1",
            entity: "CACIB-PARIS",
            status: "Unfilled",
            portfolios: [
                {
                    id: 11,
                    name: "Portfolio A",
                    times: [10, 20, 30, 40, 50, 60, 70, 80, 90, 10, 20, 30],
                },
                {
                    id: 12,
                    name: "Portfolio B",
                    times: [15, 25, 35, 45, 55, 65, 75, 85, 95, 15, 25, 35],
                },
            ],
        },
        {
            id: 2,
            name: "Trader 2",
            entity: "CACIB-NewYork",
            status: "Unfilled",
            portfolios: [
                {
                    id: 21,
                    name: "Portfolio C",
                    times: [5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 5, 15],
                },
                {
                    id: 22,
                    name: "Portfolio D",
                    times: [20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30],
                },
            ],
        },
    ];

    let months = [
        "Janvier",
        "Février",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Août",
        "Septembre",
        "Octobre",
        "Novembre",
        "Décembre",
    ];

    let currentMonth = new Date().getMonth();
    let editableMonth = currentMonth;

    function isEditable(monthIndex) {
        return monthIndex === editableMonth;
    }

    function handleChange(traderId, portfolioId, monthIndex, event) {
        const trader = traders.find((t) => t.id === traderId);
        const portfolio = trader.portfolios.find((p) => p.id === portfolioId);

        // Handle the change in time allocation for the specified month
        portfolio.times[monthIndex] = parseFloat(event.target.value);
    }

    $: isValidTotal = (trader) => {
        const currentTotal = trader.portfolios.reduce(
            (total, portfolio) => total + portfolio.times[currentMonth],
            0,
        );
        return currentTotal === 100;
    };
</script>

<h1>Business Manager</h1>
{#each traders as trader}
    <div>
        <h3>{trader.name}</h3>
        <h4>Entity: {trader.entity}</h4>
        <div
            class="status-box"
            class:statut-unfilled={trader.status === "Unfilled"}
            class:statut-saved={trader.status === "saved"}
            class:statut-submitted={trader.status === "submitted"}
        >
            {trader.status}
        </div>
        <table>
            <thead>
                <tr>
                    <th>Portefeuille</th>
                    {#each months as month, index (month)}
                        <th>{month}</th>
                    {/each}
                </tr>
            </thead>
            <tbody>
                {#each trader.portfolios as portfolio}
                    <tr>
                        <td>{portfolio.name}</td>
                        {#each months as month, monthIndex (month)}
                            <td>
                                {#if isEditable(monthIndex)}
                                    <input
                                        type="number"
                                        bind:value={portfolio.times[monthIndex]}
                                        on:input={(e) =>
                                            handleChange(
                                                trader.id,
                                                portfolio.id,
                                                monthIndex,
                                                e,
                                            )}
                                    />
                                {:else}
                                    <input
                                        type="number"
                                        value={portfolio.times[monthIndex]}
                                        readonly
                                        class:current-month={monthIndex ===
                                            currentMonth}
                                        class:valid={isValidTotal(trader) &&
                                            monthIndex === currentMonth}
                                        class:invalid={!isValidTotal(trader) &&
                                            monthIndex === currentMonth}
                                    />
                                {/if}
                            </td>
                        {/each}
                    </tr>
                {/each}
            </tbody>
            <tfoot>
                <tr class="total-row">
                    <td>Total</td>
                    {#each months as month, monthIndex (month)}
                        <td>
                            <input
                                type="number"
                                value={trader.portfolios.reduce(
                                    (total, portfolio) =>
                                        total + portfolio.times[monthIndex],
                                    0,
                                )}
                                readonly
                                class:current-month={monthIndex ===
                                    currentMonth}
                                class:valid={isValidTotal(trader) &&
                                    monthIndex === currentMonth}
                                class:invalid={!isValidTotal(trader) &&
                                    monthIndex === currentMonth}
                            />
                        </td>
                    {/each}
                </tr>
            </tfoot>
        </table>
    </div>
{/each}

<style>
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        table-layout: fixed;
    }

    th,
    td {
        border: 1px solid #ddd;
        padding: 4px; /* Réduit la taille du padding */
        text-align: center;
        width: 8.33%; /* ou une autre valeur fixe selon le nombre de colonnes */
        white-space: nowrap;
        overflow: hidden;
    }

    th {
        background-color: #f2f2f2;
    }

    input[readonly] {
        background-color: #ccc;
        width: 100%; /* Empêche l'input de dépasser la cellule */
        box-sizing: border-box; /* Inclut la bordure et le padding dans la largeur totale */
    }

    .total-row td {
        font-weight: bold;
    }

    .total-row input.current-month.invalid {
        background-color: #ff7f7f;
    }

    .total-row input.current-month.valid {
        background-color: #7fff7f;
    }

    .total-row input:not(.current-month) {
        background-color: #ccc;
    }

    .status-box {
        float: right;
        margin-left: 10px;
        width: 80px;
        height: 20px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        color: white;
    }

    .statut-unfilled {
        background-color: red;
    }
</style>
