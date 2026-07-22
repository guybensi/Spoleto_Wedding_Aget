from __future__ import annotations

from dataclasses import asdict, dataclass


class ValidationError(ValueError):
	pass


@dataclass(frozen=True)
class Itinerary:
	title: str
	day: str
	details: str


@dataclass(frozen=True)
class Transportation:
	mode: str
	departure: str
	arrival: str
	details: str


@dataclass(frozen=True)
class Accommodation:
	hotel_name: str
	address: str
	check_in: str
	check_out: str


@dataclass(frozen=True)
class Recommendations:
	category: str
	item: str
	notes: str


@dataclass(frozen=True)
class FAQ:
	question: str
	answer: str


def _require_string(value: object, field_name: str) -> str:
	text = str(value or "").strip()
	if not text:
		raise ValidationError(f"Missing required field: {field_name}")
	return text


def _build_itinerary(value: object) -> Itinerary:
	if not isinstance(value, dict):
		raise ValidationError("itinerary must be an object")
	return Itinerary(
		title=_require_string(value.get("title"), "itinerary.title"),
		day=_require_string(value.get("day"), "itinerary.day"),
		details=_require_string(value.get("details"), "itinerary.details"),
	)


def _build_transportation(value: object) -> Transportation:
	if not isinstance(value, dict):
		raise ValidationError("transportation must be an object")
	return Transportation(
		mode=_require_string(value.get("mode"), "transportation.mode"),
		departure=_require_string(value.get("departure"), "transportation.departure"),
		arrival=_require_string(value.get("arrival"), "transportation.arrival"),
		details=_require_string(value.get("details"), "transportation.details"),
	)


def _build_accommodation(value: object) -> Accommodation:
	if not isinstance(value, dict):
		raise ValidationError("accommodation must be an object")
	return Accommodation(
		hotel_name=_require_string(value.get("hotel_name"), "accommodation.hotel_name"),
		address=_require_string(value.get("address"), "accommodation.address"),
		check_in=_require_string(value.get("check_in"), "accommodation.check_in"),
		check_out=_require_string(value.get("check_out"), "accommodation.check_out"),
	)


def _build_recommendations(value: object) -> Recommendations:
	if not isinstance(value, dict):
		raise ValidationError("recommendations must be an object")
	return Recommendations(
		category=_require_string(value.get("category"), "recommendations.category"),
		item=_require_string(value.get("item"), "recommendations.item"),
		notes=_require_string(value.get("notes"), "recommendations.notes"),
	)


def _build_faq(value: object) -> FAQ:
	if not isinstance(value, dict):
		raise ValidationError("faq must be an object")
	return FAQ(
		question=_require_string(value.get("question"), "faq.question"),
		answer=_require_string(value.get("answer"), "faq.answer"),
	)


def validate_normalized_payload(payload: dict[str, object]) -> dict[str, dict[str, str]]:
	itinerary = _build_itinerary(payload.get("itinerary"))
	transportation = _build_transportation(payload.get("transportation"))
	accommodation = _build_accommodation(payload.get("accommodation"))
	recommendations = _build_recommendations(payload.get("recommendations"))
	faq = _build_faq(payload.get("faq"))

	return {
		"itinerary": asdict(itinerary),
		"transportation": asdict(transportation),
		"accommodation": asdict(accommodation),
		"recommendations": asdict(recommendations),
		"faq": asdict(faq),
	}
