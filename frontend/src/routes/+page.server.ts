import { hash, verify } from '@node-rs/argon2';
import { encodeBase32LowerCase } from '@oslojs/encoding';
import { fail, redirect } from '@sveltejs/kit';
import { eq } from 'drizzle-orm';
import * as auth from '$lib/server/auth';
import { db } from '$lib/server/db';
import * as table from '$lib/server/db/schema';
import type { Actions, PageServerLoad } from './$types';
import { loginSchema, registerSchema } from './schemas/auth';
import { superValidate, message } from 'sveltekit-superforms/server';
import { zod } from 'sveltekit-superforms/adapters';

export const load: PageServerLoad = async (event) => {
	if (event.locals.user) {
		return redirect(302, '/dashboard');
	}

	return {
		loginForm: await superValidate(zod(loginSchema)),
		registerForm: await superValidate(zod(registerSchema))
	};
};

export const actions: Actions = {
	login: async (event) => {
		const form = await superValidate(event, zod(loginSchema));
		
		if (!form.valid) {
			return message(form, 'Please fix the errors below', { status: 400 });
		}
		
		const { username, password } = form.data;
		
		const results = await db.select().from(table.user).where(eq(table.user.username, username));

		const existingUser = results.at(0);
		if (!existingUser) {
			return message(form, 'Incorrect username or password', { status: 400 });
		}

		const validPassword = await verify(existingUser.passwordHash, password, {
			memoryCost: 19456,
			timeCost: 2,
			outputLen: 32,
			parallelism: 1
		});
		
		if (!validPassword) {
			return message(form, 'Incorrect username or password', { status: 400 });
		}

		// Create the session and redirect to dashboard
		const sessionToken = auth.generateSessionToken();
		const session = await auth.createSession(sessionToken, existingUser.id);
		auth.setSessionTokenCookie(event, sessionToken, session.expiresAt);
		
		return redirect(302, '/dashboard');
	},
	
	register: async (event) => {
		const form = await superValidate(event, zod(registerSchema));
		
		if (!form.valid) {
			return message(form, 'Please fix the errors below', { status: 400 });
		}
		
		const { username, password } = form.data;

		// Check if username already exists
		const existingUser = await db.select()
			.from(table.user)
			.where(eq(table.user.username, username))
			.then(results => results.at(0));
			
		if (existingUser) {
			form.errors.username = ['Username already taken'];
			return message(form, 'Username already taken', { status: 400 });
		}

		const userId = generateUserId();
		const passwordHash = await hash(password, {
			memoryCost: 19456,
			timeCost: 2,
			outputLen: 32,
			parallelism: 1
		});

		try {
			// Create user account
			await db.insert(table.user).values({ id: userId, username, passwordHash });
			
			// Create session and set cookie
			const sessionToken = auth.generateSessionToken();
			const session = await auth.createSession(sessionToken, userId);
			auth.setSessionTokenCookie(event, sessionToken, session.expiresAt);
		} catch (e) {
			console.error("User creation failed:", e);
			return message(form, 'An error occurred while creating your account', { status: 500 });
		}
		
		return redirect(302, '/dashboard');
	}
};

function generateUserId() {
	const bytes = crypto.getRandomValues(new Uint8Array(15));
	const id = encodeBase32LowerCase(bytes);
	return id;
}