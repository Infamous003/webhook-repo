let lastTimestamp = null;
const eventsUrl = "/api/events";
const listElement = document.querySelector(".list-js");
const renderedEvents = new Set(); // This set keeps track of all the events renderd, and prevent duplicates

async function fetchEvents() {
  let url = eventsUrl;

  if (lastTimestamp) {
    url += `?since=${encodeURIComponent(lastTimestamp)}`;
  }
 
  try{
    const res = await fetch(url);
  
    if (!res.ok) {
      throw new Error(`HTTP error: ${res.status}`);
    }

    const events = await res.json();

    if (events.length > 0) {
      lastTimestamp = events[0].timestamp;
      appendEvents(events);
    }
  } catch (err) {
    console.Error("Failed to fetch events: ", err);
  }
}

function appendEvents(events) {
  events.forEach(event => {
    if (renderedEvents.has(event.request_id)) {
      return;
    }
    renderedEvents.add(event.request_id);

    const li = document.createElement("li");
    li.innerHTML = formatEvent(event);
    listElement.prepend(li); // newest on top
  });
}

function formatEvent(event) {
  const time = new Date(event.timestamp).toUTCString();

  if (event.action === "PUSH") {
    return `
      <span class="user">${event.author}</span>
      <span class="action push">pushed</span>
      to <span class="branch">${event.to_branch}</span>
      <span class="time">on ${time}</span>
    `;
  }

  if (event.action === "PULL_REQUEST") {
    return `
      <span class="user">${event.author}</span> submitted a 
      <span class="action pr">pull request</span>
      from <span class="branch">${event.from_branch}</span>
      to <span class="branch">${event.to_branch}</span>
      <span class="time">on ${time}</span>
    `;
  }

  return "Unknown event";
}

// Initial fetch
fetchEvents()
// Polling the backend ap every 15 seconds for new events
setInterval(fetchEvents, 15000)