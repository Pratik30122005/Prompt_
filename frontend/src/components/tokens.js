// Dala type scale, verbatim from the style reference.
//
// The system trusts scale, never weight: 400 carries both the 113px display and the headings,
// 200 carries 18px body, 600 is only for 14px uppercase nav labels. Tracking is given in the
// spec as px per step (-4.52px at 113px, -3.12px at 78px, -1.68px at 42/48px) which is a flat
// -0.04em, so it is written as em here and stays correct under clamp().
export const CAPTION = { fontSize: 12, lineHeight: 1.5, fontWeight: 400 };
export const LABEL = { fontSize: 14, lineHeight: 1.2, letterSpacing: '0.35px', fontWeight: 600 };
export const BODY = { fontSize: 18, lineHeight: 1.5, fontWeight: 200 };
export const HEADING_2XS = { fontSize: 24, lineHeight: 1.25, letterSpacing: '-0.48px', fontWeight: 400 };
export const HEADING_XS = { fontSize: 27, lineHeight: 1, fontWeight: 400 };
export const SUBHEADING = { fontSize: 36, lineHeight: 1.2, fontWeight: 400 };

// Display steps are fluid: the spec's fixed px is the upper bound, -0.04em holds all the way down.
const fluid = (min, max) => ({
  fontSize: `clamp(${min}px, ${(max / 12.8).toFixed(2)}vw, ${max}px)`,
  lineHeight: 1.1,
  letterSpacing: '-0.04em',
  fontWeight: 400,
});
export const HEADING_SM = { ...fluid(30, 42), lineHeight: 1.2 };
export const HEADING = fluid(32, 48);
export const HEADING_LG = fluid(42, 78);
export const DISPLAY = fluid(48, 113);

// 6px base unit. Section gaps run 60-120px, element gaps 6-18px.
export const S = { 6: 6, 12: 12, 18: 18, 24: 24, 30: 30, 36: 36, 60: 60, 96: 96, 120: 120 };

// Buttons, cards and nav all share 24px; tags are full pills.
export const RADIUS = 24;
export const PILL = { ...LABEL, borderRadius: RADIUS, height: 45 };
