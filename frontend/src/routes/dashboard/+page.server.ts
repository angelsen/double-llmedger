import { fail, redirect } from '@sveltejs/kit';
import * as auth from '$lib/server/auth';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async (event) => {
	if (!event.locals.user) {
		return redirect(302, '/');
	}
	return { user: event.locals.user };
};

export const actions: Actions = {
	logout: async (event) => {
		if (!event.locals.session) {
			return fail(401);
		}
		await auth.invalidateSession(event.locals.session.id);
		auth.deleteSessionTokenCookie(event);

		return redirect(302, '/');
	},
	
	// Sign out from all devices
	logoutAll: async (event) => {
		if (!event.locals.user) {
			return fail(401);
		}
		
		try {
			// 1. Call the backend API to invalidate sessions there too
			const response = await fetch('http://localhost:8000/api/security/logout-all-devices', {
				method: 'POST',
				credentials: 'include', // Include cookies for authentication
				headers: {
					'Content-Type': 'application/json'
				}
			});
			
			if (!response.ok) {
				console.error('Failed to invalidate backend sessions:', await response.text());
			}
		} catch (err) {
			console.error('Error calling backend logout API:', err);
			// Continue with frontend logout even if backend fails
		}
		
		// 2. Invalidate all sessions on the frontend
		await auth.invalidateAllUserSessions(event.locals.user.id);
		auth.deleteSessionTokenCookie(event);

		return redirect(302, '/');
	}
};