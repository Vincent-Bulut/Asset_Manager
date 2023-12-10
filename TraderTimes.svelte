<script>
	import { businessManagerStore } from './store.js';

	// Subscribe to the store and get the current value
	const businessManagerData = $businessManagerStore;

	// Extract traders from the data
	const traders = $businessManagerStore.traders || [];

	export let cdrs;

	const monthNames = [
		'Jan',
		'Feb',
		'Mar',
		'Apr',
		'May',
		'Jun',
		'Jul',
		'Aug',
		'Sep',
		'Oct',
		'Nov',
		'Dec'
	];

	let currentMonth = new Date().getMonth();
	let editableMonth = currentMonth;

	function isEditable(monthIndex) {
		return monthIndex === editableMonth;
	}

	$: isValidTotal = (cdrs) => {
        const currentTotal = cdrs.reduce(
            (total, cdr) => total + cdr.times[currentMonth],
            0,
        );
        return currentTotal === 100;
    };

</script>

<main>
	<table>
		<thead>
			<tr>
				<th>CDR</th>
				{#each monthNames as month}
					<th>{month}</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each cdrs as cdr}
				<tr>
					<td>{cdr.name}</td>
					{#each cdr.times as time, i (time)}
						<td>
							{#if isEditable(i)}
								<input type="number" bind:value={cdr.times[i]} />
							{:else}
								<input
									type="number"
									value={cdr.times[i]}
									readonly
									class:current-month={i === currentMonth}
								/>
							{/if}
						</td>
					{/each}
				</tr>
			{/each}
		</tbody>
		<!--
		<tfoot>
			<tr class="total-row">
				<td>Total</td>
				{#each monthNames as month, monthIndex (month)}
					<td>
						<input
							type="number"
							value={cdrs.reduce(
								(total, cdr) =>
									total + cdr.times[monthIndex],
								0,
							)}
							readonly
							class:current-month={monthIndex ===
								currentMonth}
							class:valid={isValidTotal(cdrs) &&
								monthIndex === currentMonth}
							class:invalid={!isValidTotal(cdrs) &&
								monthIndex === currentMonth}
						/>
					</td>
				{/each}
			</tr>
		</tfoot>
		-->
	</table>
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
        align-items: flex-start; /* Adjusted alignment to flex-start */
        padding: 0px;
    }

    table {
        width: 800px;
        border-collapse: collapse;
        margin-top: 2px;
        margin-left: 0;
        overflow-x: auto;
        table-layout: fixed;
    }

    th, td {
        border: 1px solid #ddd;
        padding: 3px;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        font-size: 12px;
    }

    th {
        background-color: #f2f2f2;
    }

    input[readonly], input {
        width: 80%;
        box-sizing: border-box;
        text-align: center;
        font-size: 12px;
    }

    input[readonly] {
        background-color: #ccc;
    }

	/*
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
	*/
</style>



