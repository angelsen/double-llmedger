<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import * as Card from '$lib/components/ui/card';
	import * as Tabs from '$lib/components/ui/tabs';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { ThemeToggle } from '$lib/components/theme-toggle';
	import { Logo } from '$lib/components/logo';
	import { loginSchema, registerSchema } from './schemas/auth';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	
	const loginForm = superForm(data.loginForm, {
		validators: zodClient(loginSchema),
		resetForm: false,
		id: 'login-form'
	});
	
	const registerForm = superForm(data.registerForm, {
		validators: zodClient(registerSchema),
		resetForm: true,
		id: 'register-form'
	});
	
	// Destructure what we need from the forms
	const { form: loginData, enhance: loginEnhance, errors: loginErrors, message: loginMessage } = loginForm;
	const { form: registerData, enhance: registerEnhance, errors: registerErrors, message: registerMessage } = registerForm;
	
	// Default active tab
	let activeTab = $state('login');
</script>

<div class="flex min-h-screen items-center justify-center">
	<Card.Root class="w-full max-w-md">
		<Card.Header>
			<div class="flex justify-center mb-2">
				<Logo size="lg" class="mb-1" />
			</div>
			<Card.Description class="text-center">Sign in to your account to manage your finances</Card.Description>
		</Card.Header>
		<Card.Content>
			<Tabs.Root value={activeTab} onValueChange={(val) => activeTab = val}>
				<Tabs.List class="grid w-full grid-cols-2 mb-6">
					<Tabs.Trigger value="login">Login</Tabs.Trigger>
					<Tabs.Trigger value="register">Register</Tabs.Trigger>
				</Tabs.List>
				
				<Tabs.Content value="login">
					<form method="post" action="?/login" use:loginEnhance class="space-y-4">
						<div class="space-y-2">
							<label for="login-username" class="text-sm font-medium">Username</label>
							<Input 
								id="login-username" 
								name="username" 
								placeholder="Enter your username" 
								bind:value={$loginData.username}
							/>
							{#if $loginErrors.username}
								<p class="text-sm text-red-500">{$loginErrors.username}</p>
							{/if}
						</div>
						<div class="space-y-2">
							<label for="login-password" class="text-sm font-medium">Password</label>
							<Input 
								id="login-password" 
								type="password" 
								name="password" 
								placeholder="Enter your password" 
								bind:value={$loginData.password}
							/>
							{#if $loginErrors.password}
								<p class="text-sm text-red-500">{$loginErrors.password}</p>
							{/if}
						</div>
						{#if $loginMessage}
							<p class="text-sm text-red-500 mt-1">{$loginMessage}</p>
						{/if}
						<Button type="submit" class="w-full">Login</Button>
					</form>
				</Tabs.Content>
				
				<Tabs.Content value="register">
					<form method="post" action="?/register" use:registerEnhance class="space-y-4">
						<div class="space-y-2">
							<label for="register-username" class="text-sm font-medium">Username</label>
							<Input 
								id="register-username" 
								name="username" 
								placeholder="Choose a username" 
								bind:value={$registerData.username}
							/>
							{#if $registerErrors.username}
								<p class="text-sm text-red-500">{$registerErrors.username}</p>
							{/if}
						</div>
						<div class="space-y-2">
							<label for="register-password" class="text-sm font-medium">Password</label>
							<Input 
								id="register-password" 
								type="password" 
								name="password" 
								placeholder="Create a password" 
								bind:value={$registerData.password}
							/>
							{#if $registerErrors.password}
								<p class="text-sm text-red-500">{$registerErrors.password}</p>
							{/if}
						</div>
						{#if $registerMessage}
							<p class="text-sm text-red-500 mt-1">{$registerMessage}</p>
						{/if}
						<Button type="submit" class="w-full">Create Account</Button>
					</form>
				</Tabs.Content>
			</Tabs.Root>
		</Card.Content>
		<Card.Footer class="flex flex-col items-center gap-2 text-sm text-gray-500">
			<p>Secure double-entry accounting system powered by AI</p>
				<div class="mt-2"><ThemeToggle /></div>
		</Card.Footer>
	</Card.Root>
</div>