import React, { useEffect, useState } from "react";
import { Alert, Button, Form, Modal, Table, Spinner } from "react-bootstrap";
import { Link, useNavigate, useParams } from "react-router-dom";
import { request, allCategories } from "../services/TrackerService";
import AdminContent from "../commons/AdminContent";

const message = (e) => {
  const detail = e.response?.data?.detail;
  return Array.isArray(detail)
    ? detail.map((x) => `${x.loc.at(-1)}: ${x.msg}`).join("; ")
    : typeof detail === "string"
      ? detail
      : "Unable to reach the API. Check the server and try again.";
};
const statuses = ["open", "in_progress", "resolved", "closed"];
const priorities = ["low", "medium", "high", "critical"];
const label = (value) => value.replaceAll("_", " ");
function Field({
  name,
  title,
  value,
  change,
  options,
  required = false,
  maxLength,
  multiline = false,
}) {
  return (
    <Form.Group className="mb-3" controlId={name}>
      <Form.Label>
        {title}
        {required ? " *" : ""}
      </Form.Label>
      {options ? (
        <Form.Select
          value={value ?? ""}
          onChange={(e) => change(name, e.target.value)}
          required={required}
        >
          {options.map(([v, t]) => (
            <option key={v} value={v}>
              {t}
            </option>
          ))}
        </Form.Select>
      ) : (
        <Form.Control
          as={multiline ? "textarea" : "input"}
          value={value ?? ""}
          maxLength={maxLength}
          required={required}
          onChange={(e) => change(name, e.target.value)}
        />
      )}
    </Form.Group>
  );
}
function Confirm({ item, cancel, remove, busy }) {
  return (
    <Modal show={!!item} onHide={cancel}>
      <Modal.Header closeButton>
        <Modal.Title>Confirm deletion</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        Delete {item?.title || item?.name}? This cannot be undone.
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={cancel}>
          Cancel
        </Button>
        <Button variant="danger" disabled={busy} onClick={remove}>
          Confirm delete
        </Button>
      </Modal.Footer>
    </Modal>
  );
}
export function Categories() {
  const [rows, setRows] = useState([]),
    [form, setForm] = useState({ name: "", description: "" }),
    [error, setError] = useState(""),
    [loading, setLoading] = useState(true),
    [busy, setBusy] = useState(false),
    [item, setItem] = useState(null);
  const load = async () => {
    setLoading(true);
    try {
      setRows(await allCategories());
    } catch (e) {
      setError(message(e));
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    load();
  }, []);
  const change = (key, value) => setForm((f) => ({ ...f, [key]: value }));
  const save = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      await request(
        form.id ? "patch" : "post",
        form.id ? `/categories/${form.id}` : "/categories",
        { name: form.name, description: form.description },
      );
      setForm({ name: "", description: "" });
      await load();
    } catch (e) {
      setError(message(e));
    } finally {
      setBusy(false);
    }
  };
  const remove = async () => {
    setBusy(true);
    setError("");
    try {
      await request("delete", `/categories/${item.id}`);
      setItem(null);
      await load();
    } catch (e) {
      setItem(null);
      setError(message(e));
    } finally {
      setBusy(false);
    }
  };
  return (
    <AdminContent title="Category management">
      <h1>Categories</h1>
      {error && <Alert variant="danger">{error}</Alert>}
      <Form onSubmit={save}>
        <Field
          name="name"
          title="Name"
          value={form.name}
          change={change}
          required
          maxLength={100}
        />
        <Field
          name="description"
          title="Description"
          value={form.description}
          change={change}
          multiline
          maxLength={500}
        />
        <Button type="submit" disabled={busy}>
          {form.id ? "Save category" : "Create category"}
        </Button>
        {form.id && (
          <Button
            variant="secondary"
            onClick={() => setForm({ name: "", description: "" })}
          >
            Cancel edit
          </Button>
        )}
      </Form>
      {loading ? (
        <Spinner aria-label="Loading categories" />
      ) : (
        <Table responsive>
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id}>
                <td>{row.name}</td>
                <td>{row.description}</td>
                <td>
                  <Button onClick={() => setForm(row)}>Edit</Button>{" "}
                  <Button variant="danger" onClick={() => setItem(row)}>
                    Delete
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
      {!loading && !rows.length && (
        <p>No categories yet. Create one before adding issues.</p>
      )}
      <Confirm
        item={item}
        cancel={() => setItem(null)}
        remove={remove}
        busy={busy}
      />
    </AdminContent>
  );
}
const emptyFilters = {
  search: "",
  status: "",
  priority: "",
  category_id: "",
  assigned_user_id: "",
};
export function Issues() {
  const [data, setData] = useState({ records: [] }),
    [filters, setFilters] = useState(emptyFilters),
    [applied, setApplied] = useState(emptyFilters),
    [page, setPage] = useState(1),
    [cats, setCats] = useState([]),
    [users, setUsers] = useState([]),
    [error, setError] = useState(""),
    [loading, setLoading] = useState(true),
    [item, setItem] = useState(null),
    [busy, setBusy] = useState(false),
    [refresh, setRefresh] = useState(0);
  useEffect(() => {
    Promise.all([allCategories(), request("get", "/assignees")])
      .then(([c, u]) => {
        setCats(c);
        setUsers(u);
      })
      .catch((e) => setError(message(e)));
  }, []);
  useEffect(() => {
    let active = true;
    setLoading(true);
    request("get", "/issues", undefined, {
      ...Object.fromEntries(Object.entries(applied).filter(([, v]) => v)),
      page,
    })
      .then((d) => {
        if (active) setData(d);
      })
      .catch((e) => {
        if (active) setError(message(e));
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [applied, page, refresh]);
  const change = (k, v) => setFilters((f) => ({ ...f, [k]: v }));
  const remove = async () => {
    setBusy(true);
    try {
      await request("delete", `/issues/${item.id}`);
      setItem(null);
      setPage(1);
      setRefresh((x) => x + 1);
    } catch (e) {
      setItem(null);
      setError(message(e));
    } finally {
      setBusy(false);
    }
  };
  return (
    <AdminContent title="Issue directory">
      <h1>Issues</h1>
      <Link className="btn btn-primary mb-3" to="/issues/new">
        New issue
      </Link>
      {error && <Alert variant="danger">{error}</Alert>}
      <Form
        onSubmit={(e) => {
          e.preventDefault();
          setError("");
          setPage(1);
          setApplied({ ...filters });
        }}
      >
        <Field
          name="search"
          title="Search title"
          value={filters.search}
          change={change}
        />
        <div className="row">
          {[
            ["status", "Status", statuses.map((v) => [v, label(v)])],
            ["priority", "Priority", priorities.map((v) => [v, label(v)])],
            ["category_id", "Category", cats.map((c) => [c.id, c.name])],
            [
              "assigned_user_id",
              "Assignee",
              users.map((u) => [u.id, u.full_name]),
            ],
          ].map(([k, t, o]) => (
            <div className="col-md-3" key={k}>
              <Field
                name={k}
                title={t}
                value={filters[k]}
                change={change}
                options={[["", "All"], ...o]}
              />
            </div>
          ))}
        </div>
        <Button type="submit">Apply filters</Button>{" "}
        <Button
          variant="secondary"
          onClick={() => {
            setFilters(emptyFilters);
            setApplied(emptyFilters);
            setPage(1);
          }}
        >
          Reset filters
        </Button>
      </Form>
      {loading ? (
        <Spinner aria-label="Loading issues" />
      ) : (
        <Table responsive>
          <thead>
            <tr>
              {[
                "Title",
                "Category",
                "Status",
                "Priority",
                "Assignee",
                "Updated",
                "Actions",
              ].map((h) => (
                <th key={h}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.records.map((row) => (
              <tr key={row.id}>
                <td>
                  <Link to={`/issues/${row.id}`}>{row.title}</Link>
                </td>
                <td>{row.category.name}</td>
                <td>{label(row.status)}</td>
                <td>{row.priority}</td>
                <td>{row.assigned_user?.full_name || "Unassigned"}</td>
                <td>{new Date(row.updated_at).toLocaleString()}</td>
                <td>
                  <Link to={`/issues/${row.id}/edit`}>Edit</Link>{" "}
                  <Button variant="danger" onClick={() => setItem(row)}>
                    Delete
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
      {!loading && !data.records.length && (
        <p>No issues match the selected filters.</p>
      )}
      <Button
        disabled={!data.prev_page || loading}
        onClick={() => setPage(data.prev_page)}
      >
        Previous
      </Button>{" "}
      Page {page}{" "}
      <Button
        disabled={!data.next_page || loading}
        onClick={() => setPage(data.next_page)}
      >
        Next
      </Button>
      <Confirm
        item={item}
        cancel={() => setItem(null)}
        remove={remove}
        busy={busy}
      />
    </AdminContent>
  );
}
export function IssueForm() {
  const { id } = useParams(),
    navigate = useNavigate();
  const [form, setForm] = useState({
      title: "",
      description: "",
      status: "open",
      priority: "medium",
      category_id: "",
      assigned_user_id: "",
    }),
    [cats, setCats] = useState([]),
    [users, setUsers] = useState([]),
    [error, setError] = useState(""),
    [ready, setReady] = useState(false),
    [busy, setBusy] = useState(false);
  useEffect(() => {
    Promise.all([
      allCategories(),
      request("get", "/assignees"),
      id ? request("get", `/issues/${id}`) : Promise.resolve(null),
    ])
      .then(([c, u, i]) => {
        setCats(c);
        setUsers(u);
        if (i) setForm(i);
        setReady(true);
      })
      .catch((e) => setError(message(e)));
  }, [id]);
  const change = (k, v) => setForm((f) => ({ ...f, [k]: v }));
  const save = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    const payload = Object.fromEntries(
      [
        "title",
        "description",
        "status",
        "priority",
        "category_id",
        "assigned_user_id",
      ].map((k) => [k, k === "assigned_user_id" ? form[k] || null : form[k]]),
    );
    try {
      const result = await request(
        id ? "patch" : "post",
        id ? `/issues/${id}` : "/issues",
        payload,
      );
      navigate(`/issues/${result.id}`);
    } catch (e) {
      setError(message(e));
    } finally {
      setBusy(false);
    }
  };
  return (
    <>
      <h1>{id ? "Edit issue" : "New issue"}</h1>
      {error && <Alert variant="danger">{error}</Alert>}
      {!ready && !error && <Spinner aria-label="Loading form" />}
      {ready && (
        <Form onSubmit={save}>
          <Field
            name="title"
            title="Title"
            value={form.title}
            change={change}
            required
            maxLength={200}
          />
          <Field
            name="description"
            title="Description"
            value={form.description}
            change={change}
            multiline
            maxLength={5000}
          />
          <Field
            name="status"
            title="Status"
            value={form.status}
            change={change}
            options={statuses.map((v) => [v, label(v)])}
            required
          />
          <Field
            name="priority"
            title="Priority"
            value={form.priority}
            change={change}
            options={priorities.map((v) => [v, v])}
            required
          />
          <Field
            name="category_id"
            title="Category"
            value={form.category_id}
            change={change}
            options={[
              ["", "Choose a category"],
              ...cats.map((c) => [c.id, c.name]),
            ]}
            required
          />
          <Field
            name="assigned_user_id"
            title="Assignee"
            value={form.assigned_user_id}
            change={change}
            options={[
              ["", "Unassigned"],
              ...users.map((u) => [u.id, u.full_name]),
            ]}
          />
          {!cats.length && (
            <Alert variant="warning">Create a category first.</Alert>
          )}
          <Button type="submit" disabled={busy || !cats.length}>
            Save issue
          </Button>{" "}
          <Link to="/issues">Cancel</Link>
        </Form>
      )}
    </>
  );
}
export function IssueDetails() {
  const { id } = useParams();
  const [issue, setIssue] = useState(null),
    [error, setError] = useState("");
  useEffect(() => {
    request("get", `/issues/${id}`)
      .then(setIssue)
      .catch((e) => setError(message(e)));
  }, [id]);
  return (
    <>
      {error && <Alert variant="danger">{error}</Alert>}
      {!issue && !error && <Spinner aria-label="Loading issue" />}
      {issue && (
        <>
          <h1>{issue.title}</h1>
          <p style={{ whiteSpace: "pre-wrap" }}>{issue.description}</p>
          <dl>
            {[
              ["Category", issue.category.name],
              ["Status", label(issue.status)],
              ["Priority", issue.priority],
              ["Assignee", issue.assigned_user?.full_name || "Unassigned"],
              ["Updated", new Date(issue.updated_at).toLocaleString()],
            ].map(([k, v]) => (
              <React.Fragment key={k}>
                <dt>{k}</dt>
                <dd>{v}</dd>
              </React.Fragment>
            ))}
          </dl>
          <Link className="btn btn-primary" to={`/issues/${id}/edit`}>
            Edit issue
          </Link>{" "}
        </>
      )}
      <Link to="/issues">Back to issues</Link>
    </>
  );
}
