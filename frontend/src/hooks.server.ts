import type { Handle } from '@sveltejs/kit';
import * as auth from '$lib/server/auth.js';
import { env } from '$env/dynamic/private';

// Allowed origin for CSRF protection
const ALLOWED_ORIGIN = env.ALLOWED_ORIGIN || (process.env.NODE_ENV === 'production' 
    ? 'https://yourdomain.com' // Replace with your production domain
    : 'http://localhost:5173'); // Default SvelteKit dev server

const handleCSRF: Handle = async ({ event, resolve }) => {
    // CSRF protection for non-GET requests
    if (event.request.method !== 'GET') {
        const origin = event.request.headers.get('origin');
        // If no origin header or origin doesn't match our site, reject the request
        if (!origin || origin !== ALLOWED_ORIGIN) {
            return new Response('CSRF check failed', { status: 403 });
        }
    }
    
    return resolve(event);
};

const handleAuth: Handle = async ({ event, resolve }) => {
	const sessionToken = event.cookies.get(auth.sessionCookieName);
	if (!sessionToken) {
		event.locals.user = null;
		event.locals.session = null;
		return resolve(event);
	}

	const { session, user } = await auth.validateSessionToken(sessionToken);
	if (session) {
		auth.setSessionTokenCookie(event, sessionToken, session.expiresAt);
	} else {
		auth.deleteSessionTokenCookie(event);
	}

	event.locals.user = user;
	event.locals.session = session;

	return resolve(event);
};

// Apply both CSRF and auth handlers in sequence
export const handle: Handle = async ({ event, resolve }) => {
    // First check CSRF, then handle auth
    const csrfResult = await handleCSRF({ event, resolve: async (event) => {
        return handleAuth({ event, resolve });
    }});
    
    return csrfResult;
};
