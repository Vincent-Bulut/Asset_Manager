<script>
    import { businessManagerStore } from '../store.js';
    import Trader from '../Trader.svelte';
    const businessManagerData = $businessManagerStore;

    let trader = businessManagerData.traders[1];

    function publish() {
		// Handle publish logic
		//businessManagerData.time_status = 'Published';
		console.log('Publish button clicked ${businessManagerData.time_status}');
	}
</script>

<main>
    <Trader trader={trader} />
    <div class="button-container">
		<button class="button" on:click={publish}>Clone</button>
		<button class="button" on:click={publish}>Publish</button>
		<button class="button" on:click={publish}>Help</button>
	</div>
</main>

<style>
    .button-container {
		margin-top: 15px;
		display: flex;
		gap: 10px;
	}

	.button {
		padding: 10px;
		background-color: #333;
		color: white;
		border: none;
		border-radius: 5px;
		cursor: pointer;
	}
</style>