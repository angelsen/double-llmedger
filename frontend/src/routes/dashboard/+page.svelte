<script lang="ts">
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card';
	import * as Tabs from '$lib/components/ui/tabs';
	import { Button } from '$lib/components/ui/button';
	import { ThemeToggle } from '$lib/components/theme-toggle';
	import { Logo } from '$lib/components/logo';
	import type { PageServerData } from './$types';

	let { data }: { data: PageServerData } = $props();
	
	// Define transaction type
	interface Transaction {
		id: string;
		date: string;
		amount: number;
		type: string;
		description: string;
	}
	
	// Dashboard data from API
	let apiData = $state({
		account_balance: 0,
		upcoming_bills: 0,
		monthly_savings: 0,
		recent_transactions: [] as Transaction[],
		account_name: '',
		loading: true,
		error: null as string | null
	});
	
	onMount(async () => {
		try {
			// Fetch data from our FastAPI backend
			const response = await fetch('http://localhost:8000/api/dashboard-data', {
				credentials: 'include' // Include cookies for authentication
			});
			
			if (!response.ok) {
				throw new Error(`API error: ${response.status}`);
			}
			
			const dashboardData = await response.json();
			apiData = {
				...dashboardData,
				loading: false,
				error: null
			};
		} catch (err) {
			const error = err as Error;
			console.error('Failed to fetch dashboard data:', error);
			apiData.loading = false;
			apiData.error = error.message || 'Unknown error';
		}
	});
</script>

<div class="container mx-auto p-4">
	<header class="flex justify-between items-center mb-8">
		<div class="flex items-center">
			<Logo variant="dashboard" size="md" />
		</div>
		<div class="flex items-center gap-4">
			<span>Welcome, {data.user.username}</span>
			<form method="post" action="?/logout">
				<Button variant="outline" type="submit">Logout</Button>
			</form>
			<ThemeToggle />
		</div>
	</header>

	<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
		<Card.Root>
			<Card.Header>
				<Card.Title>Account Balance</Card.Title>
				<Card.Description>Current financial status</Card.Description>
			</Card.Header>
			<Card.Content>
				{#if apiData.loading}
					<p class="text-3xl font-bold">Loading...</p>
				{:else if apiData.error}
					<p class="text-lg text-red-500">Failed to load data</p>
				{:else}
					<p class="text-3xl font-bold">${apiData.account_balance.toFixed(2)}</p>
				{/if}
			</Card.Content>
		</Card.Root>
		
		<Card.Root>
			<Card.Header>
				<Card.Title>Upcoming Bills</Card.Title>
				<Card.Description>Due in the next 30 days</Card.Description>
			</Card.Header>
			<Card.Content>
				{#if apiData.loading}
					<p class="text-3xl font-bold">Loading...</p>
				{:else if apiData.error}
					<p class="text-lg text-red-500">Failed to load data</p>
				{:else}
					<p class="text-3xl font-bold">${apiData.upcoming_bills.toFixed(2)}</p>
				{/if}
			</Card.Content>
		</Card.Root>
		
		<Card.Root>
			<Card.Header>
				<Card.Title>Monthly Savings</Card.Title>
				<Card.Description>Current month progress</Card.Description>
			</Card.Header>
			<Card.Content>
				{#if apiData.loading}
					<p class="text-3xl font-bold">Loading...</p>
				{:else if apiData.error}
					<p class="text-lg text-red-500">Failed to load data</p>
				{:else}
					<p class="text-3xl font-bold">${apiData.monthly_savings.toFixed(2)}</p>
				{/if}
			</Card.Content>
		</Card.Root>
	</div>

	<Tabs.Root value="transactions">
		<Tabs.List class="grid grid-cols-4 w-full max-w-md mb-8">
			<Tabs.Trigger value="transactions">Transactions</Tabs.Trigger>
			<Tabs.Trigger value="invoices">Invoices</Tabs.Trigger>
			<Tabs.Trigger value="reports">Reports</Tabs.Trigger>
			<Tabs.Trigger value="settings">Settings</Tabs.Trigger>
		</Tabs.List>
		
		<Tabs.Content value="transactions">
			<div class="bg-white p-6 rounded-lg shadow-sm dark:bg-gray-800">
				<h2 class="text-xl font-semibold mb-4">Recent Transactions</h2>
				
				{#if apiData.loading}
					<p class="text-gray-500">Loading transactions...</p>
				{:else if apiData.error}
					<p class="text-red-500">Failed to load transactions: {apiData.error}</p>
				{:else if apiData.recent_transactions.length === 0}
					<p class="text-gray-500">No transactions recorded yet.</p>
				{:else}
					<div class="overflow-x-auto">
						<table class="w-full border-collapse">
							<thead class="bg-gray-100 dark:bg-gray-700">
								<tr>
									<th class="p-2 text-left">Date</th>
									<th class="p-2 text-left">Description</th>
									<th class="p-2 text-left">Type</th>
									<th class="p-2 text-right">Amount</th>
								</tr>
							</thead>
							<tbody>
								{#each apiData.recent_transactions as transaction}
									<tr class="border-b border-gray-200 dark:border-gray-700">
										<td class="p-2">
											{new Date(transaction.date).toLocaleDateString()}
										</td>
										<td class="p-2">{transaction.description}</td>
										<td class="p-2">{transaction.type}</td>
										<td class="p-2 text-right" class:text-red-500={transaction.amount < 0} class:text-green-500={transaction.amount > 0}>
											${Math.abs(transaction.amount).toFixed(2)}
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				{/if}
				
				<div class="mt-4">
					<Button>Add Transaction</Button>
				</div>
			</div>
		</Tabs.Content>

		
		<Tabs.Content value="invoices">
			<div class="bg-white p-6 rounded-lg shadow-sm dark:bg-gray-800">
				<h2 class="text-xl font-semibold mb-4">Invoice Management</h2>
				<p class="text-gray-500">No invoices uploaded. Upload your first invoice for processing.</p>
				<div class="mt-4">
					<Button>Upload Invoice</Button>
				</div>
			</div>
		</Tabs.Content>
		
		<Tabs.Content value="reports">
			<div class="bg-white p-6 rounded-lg shadow-sm dark:bg-gray-800">
				<h2 class="text-xl font-semibold mb-4">Financial Reports</h2>
				<p class="text-gray-500">Add transaction data to generate reports.</p>
			</div>
		</Tabs.Content>
		
		<Tabs.Content value="settings">
			<div class="bg-white p-6 rounded-lg shadow-sm dark:bg-gray-800">
				<h2 class="text-xl font-semibold mb-4">Account Settings</h2>
				<div class="space-y-6">
					<div>
						<h3 class="text-lg font-medium mb-2">Security</h3>
						<div class="flex flex-col space-y-2">
							<form method="post" action="?/logoutAll">
								<Button variant="destructive" type="submit">
									Logout from all devices
								</Button>
							</form>
							<p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
								This will sign you out from all your active sessions on all devices.
							</p>
						</div>
					</div>
					<p class="text-gray-500">Manage your account preferences and connections.</p>
				</div>
			</div>
		</Tabs.Content>
	</Tabs.Root>
</div>