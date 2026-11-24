# Portal design QA

## Target and scope

- Primary direction: the selected learning-workspace concept, adapted to English left-to-right reading.
- Additional reference inspected: the live Rafeeq setup screenshot supplied by the root agent.
- Preserved design: navy course header, a calm sidebar, white reading surface, teal actions, generous section spacing, and visible expected results.
- Adaptations requested by the user: all student-facing copy in English; a dedicated route for each day; five-day cumulative data-engineering project.

## Functional checks completed locally

- Production Vite build completes.
- Six metrics comparison unit checks pass for exact values, wrong envelopes, type mismatches, missing keys, array order, and extra-field disclosure.
- Four starter runtime checks pass, including static assets, route fallback, and packaging.
- The published content inputs contain exactly 20 slides per day, with the activity, activity explanation, lab, outputs, question, and answer in slots 9, 10, 17, 18, 19, and 20.
- All image and font content is local or bundled. The primary reference contains no required illustration assets.
- Body explanation copy is 16px across desktop and mobile; regular interface labels are at least 14px.

## Browser checks observed by the root agent

- The exact managed-preview URL rendered successfully in the cloud browser.
- Desktop home: clean layout, English left-to-right content, and accurate navigation.
- Setup: all four guided steps were exercised, including Next through the final Save routine.
- Day 2 Learn: correct daily context and activity content rendered.

## Browser checks still to complete with the root agent

- Mobile layout inspection and the latest classroom reading-size adjustments.
- Remaining daily tabs, answer reveals, comparison file input, local checklists, search, submission helper, and slides 19–20.
- Browser console review and final rendered-document checks.

## Preview environment

- The managed preview command was restarted against this exact `site/` checkout.
- Its returned URL is `http://127.0.0.1:4173/`. The managed-preview instructions require opening that exact URL in the cloud browser.
- A rewritten `terminal.local` URL did not render. Using the exact CLI URL resolved the routing issue.
- The final browser result must be recorded below after the remaining interaction review.

final result: review in progress

Desktop home, setup, and Day 2 Learn have been observed successfully. Mobile and the remaining functional checks are pending; this file does not yet record a complete visual pass.
