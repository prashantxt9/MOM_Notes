

MOM Notes —
Nombre del producto: MOM Notes
Objetivo: construir desde cero una aplicación local, multiplataforma y open source para grabar, importar, transcribir, resumir, organizar y consultar reuniones, audios y vídeos.
Principio principal: procesamiento local por defecto, arquitectura modular y adaptadores intercambiables para sistema operativo, GPU, motor de transcripción, diarización y modelo de lenguaje.

1. Instrucciones generales para Codex
Construye este proyecto desde cero. No copies código, estructura, recursos, nombres internos ni interfaz de otros productos. Se pueden implementar funcionalidades equivalentes, pero con una arquitectura propia.

Trabaja de forma incremental y mantén siempre el proyecto ejecutable.

Reglas de desarrollo
Usa Python 3.11 o superior.

El backend principal será FastAPI.

La base de datos será SQLite.

La interfaz inicial será web local, servida por FastAPI.

Evita frameworks frontend pesados en la primera versión.

Usa Jinja2, HTML, CSS y JavaScript sencillo; HTMX es opcional.

Separa estrictamente:

dominio;

servicios;

infraestructura;

adaptadores;

API;

interfaz.

Todas las dependencias externas deben estar encapsuladas detrás de interfaces.

La aplicación debe funcionar aunque no haya GPU.

Nunca debe comenzar a grabar sin una acción explícita del usuario.

No debe enviar audio, transcripciones ni resúmenes a servicios externos salvo que el usuario configure y seleccione voluntariamente un proveedor remoto.

Incluye tests desde el principio.

Añade tipos de Python y validación con Pydantic.

Usa migraciones SQL versionadas.

Incluye logs legibles y rotativos.

No bloquees el hilo principal con transcripción, diarización, exportaciones o generación de resúmenes.

No inventes implementaciones falsas para funciones no terminadas. Cuando una capa todavía no esté disponible, devuelve un estado claro como not_supported o not_implemented.

Prioriza primero una base sólida y extensible.

Mantén comentarios, nombres de clases, nombres de funciones y documentación técnica en inglés.

La interfaz podrá estar inicialmente en inglés, pero debe preparar un sistema sencillo de internacionalización.

2. Visión del producto
La aplicación debe permitir:

Importar archivos de audio o vídeo.

Grabar desde el micrófono.

Capturar audio del sistema mediante adaptadores específicos.

Capturar micrófono y audio del sistema simultáneamente.

Transcribir localmente.

Mostrar la transcripción mientras se procesa.

Retranscribir con otro modelo.

Separar hablantes.

Asignar nombres a los hablantes.

Generar resúmenes locales.

Extraer tareas, decisiones, fechas y preguntas.

Usar plantillas de resumen.

Editar y corregir transcripciones.

Buscar y reemplazar texto.

Exportar múltiples formatos.

Consultar reuniones mediante chat.

Integrarse con calendarios.

Detectar aplicaciones de reuniones.

Funcionar en Windows, macOS y Linux.

Elegir automáticamente la mejor aceleración disponible.

Funcionar completamente en CPU cuando no haya GPU.

3. Alcance por fases
No intentes implementar todo en una sola entrega.

Fase 0 — Base del proyecto
Crear:

estructura del repositorio;

configuración;

logging;

SQLite;

migraciones;

FastAPI;

interfaz web mínima;

health check;

sistema de trabajos;

tests básicos;

almacenamiento local multiplataforma.

La aplicación debe arrancar con:

python -m mom_notes
Y abrir:

http://127.0.0.1:8765
Fase 1 — MVP funcional
Implementar completamente:

Importación de WAV, MP3, M4A, FLAC, OGG, AAC, MP4, MKV, WebM y MOV.

Extracción/normalización de audio con FFmpeg.

Transcripción con faster-whisper.

Selección de modelo Whisper.

CPU con int8.

CUDA si está disponible.

Persistencia en SQLite.

Visualización de segmentos con timestamps.

Editor básico de transcripción.

Buscar y reemplazar.

Resumen mediante proveedor Ollama.

Proveedor OpenAI-compatible configurable.

Plantillas de resumen.

Extracción estructurada de:

resumen;

temas;

decisiones;

tareas;

responsables;

fechas;

preguntas pendientes.

Exportación TXT, Markdown, JSON, SRT y VTT.

Reprocesar y retranscribir.

Cola de trabajos.

Progreso visible.

Cancelación de trabajos.

Historial de reuniones.

Eliminación segura de reuniones y archivos.

Fase 2 — Grabación local
Implementar:

Grabación de micrófono desde navegador con MediaRecorder.

Selección de dispositivo.

Indicador de nivel de audio.

Pausar y reanudar.

Guardar audio en fragmentos.

Recuperación después de un cierre inesperado.

Conversión automática a WAV mono compatible con transcripción.

Transcripción incremental después de cada bloque.

Transcripción provisional y confirmada.

Guardado periódico.

El navegador debe enviar fragmentos al backend cada pocos segundos.

Fase 3 — Diarización y hablantes
Implementar:

Interfaz DiarizationEngine.

Adaptador para pyannote.audio.

Procesamiento posterior a la grabación.

Alineación de segmentos de transcripción con segmentos de hablante.

Etiquetas:

SPEAKER_00;

SPEAKER_01;

etc.

Renombrar hablantes.

Aplicar un nombre a todas sus intervenciones.

Guardar perfiles de voz opcionales.

Interfaz SpeakerRecognitionEngine.

Posibilidad de recordar una voz para reuniones futuras.

Umbral de confianza configurable.

No asignar automáticamente un nombre si la confianza es baja.

Mostrar siempre la puntuación de confianza.

La diarización en tiempo real no es obligatoria inicialmente. La estrategia recomendada es:

transcripción rápida durante la reunión;

diarización completa al finalizar;

realineación de la transcripción;

actualización del resultado final.

Fase 4 — Captura del audio del sistema
Crear primero la interfaz y los stubs:

class AudioCaptureBackend(Protocol):
    def list_sources(self) -> list[AudioSource]: ...
    async def start(self, config: CaptureConfig) -> CaptureSession: ...
    async def stop(self, session_id: str) -> CaptureResult: ...
    async def pause(self, session_id: str) -> None: ...
    async def resume(self, session_id: str) -> None: ...
Adaptadores previstos:

Windows
└── WASAPI loopback

macOS
└── ScreenCaptureKit

Linux
├── PipeWire
└── PulseAudio fallback
Implementar en este orden:

Windows WASAPI.

Linux PipeWire.

macOS ScreenCaptureKit.

La aplicación debe conservar pistas separadas:

microphone.wav
system_audio.wav
mixed.wav
Añadir una capa de mezcla configurable:

volumen de micrófono;

volumen del sistema;

normalización;

prevención de clipping;

mono o estéreo;

frecuencia de muestreo;

silencio automático de pistas vacías.

Fase 5 — Modelos, GPU y aceleración
Crear detectores de capacidades.

class ComputeBackend(Protocol):
    def detect(self) -> ComputeCapabilities: ...
    def supported_transcription_profiles(self) -> list[ModelProfile]: ...
    def supported_llm_profiles(self) -> list[ModelProfile]: ...
Soportar progresivamente:

Windows
CPU.

NVIDIA CUDA.

NVIDIA con CTranslate2.

Vulkan mediante motor alternativo.

DirectML como posible adaptador futuro.

Linux
CPU.

NVIDIA CUDA.

Vulkan mediante motor alternativo.

ROCm como adaptador futuro.

macOS
CPU.

Apple Silicon.

Metal mediante motor alternativo.

CoreML o MLX como adaptador futuro.

Motores de transcripción:

FasterWhisperEngine
WhisperCppEngine
ParakeetEngine
ExternalTranscriptionApiEngine
No acoples el dominio a faster-whisper.

Crear perfiles:

fast
balanced
accurate
very_accurate
custom
Cada perfil define:

motor;

modelo;

dispositivo;

compute type;

beam size;

VAD;

batch size;

idioma;

traducción;

parámetros avanzados.

Fase 6 — Resúmenes avanzados
Proveedores:

EmbeddedLlamaCppProvider
OllamaProvider
OpenAICompatibleProvider
OpenAIProvider
AnthropicProvider
GeminiProvider
No es necesario implementar todos de inmediato. Sí deben existir las interfaces y configuración.

Implementar resumen jerárquico:

transcripción completa
→ fragmentos
→ resumen estructurado por fragmento
→ agregación intermedia
→ resumen final
La salida del LLM debe pedirse en JSON estructurado y validarse con Pydantic.

Modelo de salida recomendado:

{
  "title": "",
  "executive_summary": "",
  "topics": [],
  "decisions": [],
  "action_items": [
    {
      "task": "",
      "owner": null,
      "due_date": null,
      "source_segment_ids": []
    }
  ],
  "questions": [],
  "risks": [],
  "follow_ups": [],
  "participants": [],
  "important_dates": []
}
Añadir reintentos controlados cuando el JSON sea inválido.

Nunca eliminar la transcripción original aunque falle el resumen.

Fase 7 — Chat con reuniones
Implementar inicialmente:

SQLite FTS5.

Indexación de segmentos.

Búsqueda por palabras.

Recuperación de fragmentos relevantes.

Respuesta del LLM basada únicamente en los fragmentos recuperados.

Referencias a:

reunión;

segmento;

timestamp;

hablante.

Posteriormente añadir embeddings opcionales.

Interfaz:

class RetrievalEngine(Protocol):
    async def index_meeting(self, meeting_id: int) -> None: ...
    async def search(self, query: str, meeting_ids: list[int], limit: int) -> list[RetrievedChunk]: ...
La respuesta debe incluir citas internas:

María propuso mover el lanzamiento al viernes.

Sources:
- Reunión semanal, 00:24:18
- Reunión semanal, 00:27:03
Fase 8 — Calendario y detección de reuniones
Adaptadores:

GoogleCalendarProvider
MicrosoftCalendarProvider
ICSCalendarProvider
Funciones:

Listar próximas reuniones.

Crear una sesión a partir de un evento.

Usar el título del evento.

Importar participantes.

Elegir plantilla.

Mostrar aviso antes de la reunión.

Asociar grabación y evento.

Exportar resumen como archivo o enlace local.

Detector de reuniones:

class MeetingDetector(Protocol):
    async def detect_active_meetings(self) -> list[DetectedMeeting]: ...
Adaptadores previstos:

WindowsMeetingDetector
MacOSMeetingDetector
LinuxMeetingDetector
BrowserMeetingDetector
Aplicaciones objetivo:

Zoom.

Microsoft Teams.

Google Meet.

Webex.

Jitsi.

Slack Huddles.

Discord.

Nunca grabar automáticamente por defecto.

Comportamiento:

Parece que ha comenzado una reunión en Microsoft Teams.

[Empezar a grabar] [Ignorar] [No volver a preguntar]
Fase 9 — Aplicación de escritorio
La primera versión será web local.

Más adelante añadir un wrapper de escritorio:

Tauri
└── Python backend as sidecar
El wrapper será responsable de:

icono de bandeja;

abrir/cerrar ventana;

notificaciones;

autoarranque;

permisos del sistema;

selección de archivos;

actualización;

integraciones nativas;

detección de procesos;

captura del audio del sistema.

El backend Python seguirá siendo la fuente de verdad.

No reemplazar FastAPI ni la arquitectura Python.

4. Arquitectura propuesta
mom-notes/
├── pyproject.toml
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── .env.example
├── .gitignore
├── scripts/
│   ├── dev.py
│   ├── build.py
│   ├── download_models.py
│   └── check_environment.py
├── src/
│   └── mom_notes/
│       ├── __init__.py
│       ├── __main__.py
│       ├── bootstrap.py
│       ├── config.py
│       ├── paths.py
│       ├── logging_config.py
│       │
│       ├── domain/
│       │   ├── entities/
│       │   │   ├── meeting.py
│       │   │   ├── recording.py
│       │   │   ├── transcript.py
│       │   │   ├── speaker.py
│       │   │   ├── summary.py
│       │   │   ├── job.py
│       │   │   └── model_profile.py
│       │   ├── enums.py
│       │   ├── errors.py
│       │   └── protocols/
│       │       ├── transcription.py
│       │       ├── diarization.py
│       │       ├── speaker_recognition.py
│       │       ├── llm.py
│       │       ├── audio_capture.py
│       │       ├── calendar.py
│       │       ├── meeting_detection.py
│       │       ├── retrieval.py
│       │       └── export.py
│       │
│       ├── application/
│       │   ├── services/
│       │   │   ├── meeting_service.py
│       │   │   ├── import_service.py
│       │   │   ├── recording_service.py
│       │   │   ├── transcription_service.py
│       │   │   ├── diarization_service.py
│       │   │   ├── summary_service.py
│       │   │   ├── export_service.py
│       │   │   ├── chat_service.py
│       │   │   ├── calendar_service.py
│       │   │   └── model_manager.py
│       │   ├── commands/
│       │   ├── queries/
│       │   └── dto/
│       │
│       ├── infrastructure/
│       │   ├── database/
│       │   │   ├── connection.py
│       │   │   ├── migrations.py
│       │   │   ├── repositories/
│       │   │   └── migrations/
│       │   │       └── 001_initial.sql
│       │   ├── jobs/
│       │   │   ├── queue.py
│       │   │   ├── worker.py
│       │   │   └── events.py
│       │   ├── storage/
│       │   │   ├── meeting_storage.py
│       │   │   ├── temp_storage.py
│       │   │   └── model_storage.py
│       │   ├── ffmpeg/
│       │   │   ├── client.py
│       │   │   └── probes.py
│       │   └── security/
│       │       ├── secrets.py
│       │       └── safe_paths.py
│       │
│       ├── adapters/
│       │   ├── transcription/
│       │   │   ├── faster_whisper.py
│       │   │   ├── whisper_cpp.py
│       │   │   └── external_api.py
│       │   ├── diarization/
│       │   │   └── pyannote.py
│       │   ├── speaker_recognition/
│       │   ├── llm/
│       │   │   ├── ollama.py
│       │   │   ├── openai_compatible.py
│       │   │   └── llama_cpp.py
│       │   ├── capture/
│       │   │   ├── browser_microphone.py
│       │   │   ├── windows_wasapi.py
│       │   │   ├── macos_screencapturekit.py
│       │   │   └── linux_pipewire.py
│       │   ├── calendars/
│       │   ├── meeting_detectors/
│       │   ├── retrieval/
│       │   │   └── sqlite_fts.py
│       │   └── exporters/
│       │       ├── txt.py
│       │       ├── markdown.py
│       │       ├── json_exporter.py
│       │       ├── srt.py
│       │       ├── vtt.py
│       │       ├── pdf.py
│       │       └── docx.py
│       │
│       ├── api/
│       │   ├── app.py
│       │   ├── dependencies.py
│       │   ├── errors.py
│       │   ├── routes/
│       │   │   ├── health.py
│       │   │   ├── meetings.py
│       │   │   ├── recordings.py
│       │   │   ├── transcripts.py
│       │   │   ├── summaries.py
│       │   │   ├── jobs.py
│       │   │   ├── models.py
│       │   │   ├── settings.py
│       │   │   ├── exports.py
│       │   │   ├── chat.py
│       │   │   └── events.py
│       │   └── schemas/
│       │
│       ├── web/
│       │   ├── templates/
│       │   ├── static/
│       │   │   ├── css/
│       │   │   ├── js/
│       │   │   └── icons/
│       │   └── i18n/
│       │
│       └── cli/
│           └── main.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── api/
│   ├── fixtures/
│   └── conftest.py
└── docs/
    ├── architecture.md
    ├── database.md
    ├── adapters.md
    ├── privacy.md
    └── roadmap.md
No es obligatorio crear todos los archivos vacíos desde el primer commit. Crea primero los necesarios para la Fase 0 y ve ampliando.

5. Base de datos SQLite
Activar:

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 5000;
PRAGMA synchronous = NORMAL;
Tablas mínimas
meetings
CREATE TABLE meetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    source_type TEXT NOT NULL,
    language TEXT,
    started_at TEXT,
    ended_at TEXT,
    duration_ms INTEGER,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
recordings
CREATE TABLE recordings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    local_path TEXT NOT NULL,
    original_filename TEXT,
    media_type TEXT,
    size_bytes INTEGER,
    duration_ms INTEGER,
    sample_rate INTEGER,
    channels INTEGER,
    sha256 TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
);
Roles:

original
microphone
system_audio
mixed
normalized
transcriptions
CREATE TABLE transcriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL,
    engine TEXT NOT NULL,
    model TEXT NOT NULL,
    language TEXT,
    status TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    completed_at TEXT,
    settings_json TEXT,
    FOREIGN KEY(meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
);
transcript_segments
CREATE TABLE transcript_segments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transcription_id INTEGER NOT NULL,
    segment_index INTEGER NOT NULL,
    start_ms INTEGER NOT NULL,
    end_ms INTEGER NOT NULL,
    text TEXT NOT NULL,
    speaker_id INTEGER,
    confidence REAL,
    is_final INTEGER NOT NULL DEFAULT 1,
    metadata_json TEXT,
    FOREIGN KEY(transcription_id) REFERENCES transcriptions(id) ON DELETE CASCADE
);
speakers
CREATE TABLE speakers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER,
    stable_key TEXT,
    display_name TEXT NOT NULL,
    profile_id INTEGER,
    confidence REAL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
);
speaker_profiles
CREATE TABLE speaker_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    embedding_path TEXT,
    sample_path TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
summaries
CREATE TABLE summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL,
    transcription_id INTEGER NOT NULL,
    template_id INTEGER,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    status TEXT NOT NULL,
    content_markdown TEXT,
    structured_json TEXT,
    created_at TEXT NOT NULL,
    completed_at TEXT,
    FOREIGN KEY(meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
);
summary_templates
CREATE TABLE summary_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    system_prompt TEXT NOT NULL,
    user_prompt_template TEXT NOT NULL,
    output_schema_json TEXT,
    is_builtin INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
jobs
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT NOT NULL UNIQUE,
    meeting_id INTEGER,
    job_type TEXT NOT NULL,
    status TEXT NOT NULL,
    progress REAL NOT NULL DEFAULT 0,
    message TEXT,
    payload_json TEXT,
    result_json TEXT,
    error_text TEXT,
    created_at TEXT NOT NULL,
    started_at TEXT,
    completed_at TEXT,
    cancel_requested INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
);
settings
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
FTS5
Crear una tabla FTS para búsqueda:

CREATE VIRTUAL TABLE transcript_search USING fts5(
    meeting_id UNINDEXED,
    segment_id UNINDEXED,
    speaker_name,
    text,
    tokenize='unicode61'
);
6. Almacenamiento local
Usar platformdirs.

Estructura:

data/
├── app.db
├── meetings/
│   └── <meeting_uuid>/
│       ├── original/
│       ├── audio/
│       ├── transcript/
│       ├── summaries/
│       ├── exports/
│       └── temp/
├── models/
├── cache/
├── logs/
└── temp/
Los archivos deben usar rutas seguras.

Nunca aceptar rutas relativas externas sin resolverlas y validarlas.

7. API inicial
Sistema
GET /api/health
GET /api/info
GET /api/capabilities
GET /api/settings
PUT /api/settings
Reuniones
GET    /api/meetings
POST   /api/meetings
GET    /api/meetings/{meeting_id}
PATCH  /api/meetings/{meeting_id}
DELETE /api/meetings/{meeting_id}
Importación y grabaciones
POST /api/meetings/{meeting_id}/import
POST /api/meetings/{meeting_id}/recordings/start
POST /api/meetings/{meeting_id}/recordings/chunk
POST /api/meetings/{meeting_id}/recordings/pause
POST /api/meetings/{meeting_id}/recordings/resume
POST /api/meetings/{meeting_id}/recordings/stop
GET  /api/meetings/{meeting_id}/recordings
Transcripción
POST  /api/meetings/{meeting_id}/transcriptions
GET   /api/meetings/{meeting_id}/transcriptions
GET   /api/transcriptions/{transcription_id}
PATCH /api/transcript-segments/{segment_id}
POST  /api/transcriptions/{transcription_id}/activate
POST  /api/transcriptions/{transcription_id}/find-replace
Diarización
POST  /api/transcriptions/{transcription_id}/diarize
PATCH /api/speakers/{speaker_id}
POST  /api/speakers/{speaker_id}/remember
Resúmenes
POST /api/meetings/{meeting_id}/summaries
GET  /api/meetings/{meeting_id}/summaries
GET  /api/summaries/{summary_id}
Plantillas
GET    /api/summary-templates
POST   /api/summary-templates
PATCH  /api/summary-templates/{template_id}
DELETE /api/summary-templates/{template_id}
Chat
POST /api/chat
GET  /api/chat/sessions
Exportaciones
POST /api/meetings/{meeting_id}/exports
GET  /api/meetings/{meeting_id}/exports
GET  /api/exports/{export_id}/download
Trabajos y eventos
GET  /api/jobs
GET  /api/jobs/{job_id}
POST /api/jobs/{job_id}/cancel
GET  /api/events
Usar Server-Sent Events inicialmente para progreso.

8. Interfaz web
Pantallas mínimas:

Dashboard
Meetings
Meeting detail
New recording
Import file
Transcript editor
Speakers
Summary
Chat
Exports
Models
Settings
Dashboard
Mostrar:

reuniones recientes;

trabajos activos;

botón New recording;

botón Import audio or video;

estado de modelos;

estado de FFmpeg;

capacidades detectadas.

Detalle de reunión
Pestañas:

Overview
Recording
Transcript
Speakers
Summary
Chat
Exports
Editor de transcripción
Debe permitir:

editar un segmento;

reproducir desde un timestamp;

cambiar hablante;

seleccionar varios segmentos;

buscar;

reemplazar;

fusionar segmentos;

dividir segmentos;

activar otra transcripción;

mostrar modelo y configuración usados.

Resumen
Mostrar bloques separados:

resumen ejecutivo;

temas;

decisiones;

tareas;

responsables;

fechas;

preguntas;

riesgos;

próximos pasos.

9. Cola de trabajos
No usar Celery inicialmente.

Crear una cola local basada en:

asyncio;

ThreadPoolExecutor;

ProcessPoolExecutor cuando corresponda;

persistencia en SQLite.

Estados:

queued
running
paused
completed
failed
cancelled
Tipos:

import_media
normalize_audio
transcribe
diarize
recognize_speakers
summarize
index_search
export
download_model
El sistema debe:

persistir el trabajo;

recuperar trabajos interrumpidos;

no reanudar automáticamente operaciones no seguras;

mostrar progreso;

guardar errores;

permitir cancelación cooperativa;

limitar trabajos pesados concurrentes.

10. Gestión de modelos
Crear un ModelManager.

Funciones:

listar modelos disponibles;

listar modelos instalados;

descargar;

verificar checksum;

eliminar;

mostrar tamaño;

mostrar requisitos;

recomendar modelo;

elegir dispositivo;

comprobar memoria disponible;

comprobar espacio en disco.

No descargar modelos sin confirmación explícita.

Modelo de datos:

class ModelDescriptor(BaseModel):
    id: str
    engine: str
    display_name: str
    task: str
    size_bytes: int | None
    languages: list[str]
    devices: list[str]
    compute_types: list[str]
    source_url: str | None
    sha256: str | None
    license: str | None
11. Privacidad y seguridad
Reglas obligatorias:

Escuchar solo en 127.0.0.1 por defecto.

No habilitar acceso LAN sin configuración explícita.

No comenzar grabaciones automáticamente.

Mostrar siempre un indicador visible mientras se graba.

Guardar claves de API en el keyring del sistema.

No guardar secretos en SQLite en texto plano.

No ejecutar comandos de usuario.

Validar archivos importados.

Limitar tamaño configurable de subida.

Usar nombres internos seguros.

Limpiar archivos temporales.

No cargar pickle ni formatos inseguros de terceros.

No confiar en metadatos del archivo.

Mostrar con claridad cuándo se usará un proveedor remoto.

Antes de enviar datos a una API externa, mostrar:

proveedor;

modelo;

contenido aproximado enviado;

confirmación del usuario.

Incluir opción de borrar completamente una reunión.

Incluir política de retención local.

No incluir telemetría por defecto.

Si se añade telemetría, debe ser opt-in.

Añadir avisos de cumplimiento y consentimiento para grabaciones.

12. Dependencias iniciales
Propuesta:

dependencies = [
    "fastapi",
    "uvicorn",
    "jinja2",
    "python-multipart",
    "pydantic",
    "pydantic-settings",
    "httpx",
    "platformdirs",
    "filelock",
    "keyring",
    "faster-whisper",
    "mutagen",
    "aiofiles"
]
Desarrollo:

dev = [
    "pytest",
    "pytest-asyncio",
    "pytest-cov",
    "ruff",
    "mypy"
]
Opcionales:

diarization = [
    "pyannote.audio"
]

pdf = [
    "weasyprint"
]

docx = [
    "python-docx"
]

llama-cpp = [
    "llama-cpp-python"
]
No instales dependencias pesadas si la funcionalidad correspondiente no está activada.

13. FFmpeg
La aplicación debe:

detectar FFmpeg;

aceptar una ruta personalizada;

mostrar error útil si no existe;

incluir un modo para descargar una distribución compatible en el futuro;

no asumir que está en PATH.

Funciones mínimas:

probe_media
extract_audio
convert_to_wav
normalize_audio
mix_tracks
split_audio
generate_waveform
Formato estándar de trabajo:

PCM WAV
16 kHz o frecuencia seleccionada
mono para transcripción
float32 o s16 según motor
Conservar siempre el original.

14. Transcripción incremental
Diseñar desde el principio para soportar:

audio completo;

fragmentos;

contexto solapado;

segmentos provisionales;

segmentos definitivos;

deduplicación;

VAD;

timestamps.

No concatenar ciegamente cada resultado.

Crear un componente:

class IncrementalTranscriptMerger:
    def merge(
        self,
        previous_segments: list[TranscriptSegment],
        new_segments: list[TranscriptSegment],
        overlap_start_ms: int,
    ) -> list[TranscriptSegment]:
        ...
Debe resolver:

repeticiones;

solapamientos;

pequeñas diferencias;

palabras cortadas;

timestamps inconsistentes.

Añadir tests específicos.

15. Exportaciones
Implementar en este orden:

TXT.

Markdown.

JSON.

SRT.

VTT.

HTML.

DOCX.

PDF.

CSV.

Todos los exportadores usan una interfaz:

class MeetingExporter(Protocol):
    format_name: str
    async def export(self, request: ExportRequest) -> ExportResult: ...
Opciones:

incluir timestamps;

incluir hablantes;

incluir resumen;

incluir tareas;

incluir decisiones;

incluir transcripción completa;

incluir metadatos;

incluir audio;

crear ZIP completo.

16. Tests y calidad
Requisitos:

ruff check .

mypy src

pytest

cobertura razonable del dominio y servicios.

tests de migraciones.

tests de API.

tests de rutas.

tests de importación.

tests de deduplicación de transcripción.

tests de cancelación.

tests de proveedores usando mocks.

no usar modelos reales en tests normales.

fixtures pequeñas de audio generadas o libres.

GitHub Actions:

Windows
Linux
macOS
Jobs:

lint
typecheck
tests
package-smoke-test
17. Empaquetado
Primera distribución:

instalación Python;

pipx;

script de desarrollo.

Después:

PyInstaller por sistema operativo;

preferiblemente onedir;

instalador Windows;

paquete macOS;

AppImage o paquete Linux;

Docker opcional.

La compilación debe hacerse en cada sistema operativo. No asumir cross-compilation.

18. Criterios de aceptación del MVP
El MVP estará terminado cuando:

La aplicación arranque en Windows, macOS y Linux.

Abra la interfaz web local.

Permita importar un audio o vídeo.

Extraiga audio con FFmpeg.

Transcriba con faster-whisper.

Guarde reunión, grabación, transcripción y segmentos en SQLite.

Permita editar segmentos.

Permita buscar y reemplazar.

Genere un resumen local mediante Ollama.

Permita configurar un proveedor OpenAI-compatible.

Extraiga tareas y decisiones en JSON validado.

Exporte TXT, Markdown, JSON, SRT y VTT.

Muestre progreso.

Permita cancelar.

Mantenga un historial.

Permita borrar una reunión completamente.

Tenga tests automáticos.

No requiera GPU.

No envíe datos fuera del equipo por defecto.

Incluya documentación de instalación.

19. Orden exacto de implementación recomendado
Entrega 1
pyproject.toml;

estructura mínima;

FastAPI;

Jinja2;

configuración;

paths;

logging;

SQLite;

migraciones;

health check;

dashboard vacío;

tests.

Entrega 2
CRUD de reuniones;

almacenamiento;

importación de archivos;

FFmpeg probe;

normalización;

UI de importación;

trabajos y progreso.

Entrega 3
interfaz TranscriptionEngine;

faster-whisper;

persistencia de segmentos;

editor;

retranscripción;

perfiles.

Entrega 4
interfaz LLMProvider;

Ollama;

OpenAI-compatible;

plantillas;

resumen jerárquico;

extracción estructurada.

Entrega 5
exportadores;

FTS5;

historial;

búsqueda;

limpieza y borrado.

Entrega 6
MediaRecorder;

grabación de micrófono;

subida por fragmentos;

pausa;

recuperación;

transcripción incremental.

Entregas posteriores
diarización;

reconocimiento de hablantes;

captura del sistema;

GPU/motores alternativos;

chat;

calendario;

detección de reuniones;

Tauri;

instaladores.

20. Resultado esperado de Codex en la primera ejecución
Codex debe empezar creando una base funcional, no intentando desarrollar todas las fases.

En la primera ejecución debe:

Crear la estructura de la Fase 0.

Implementar FastAPI.

Implementar SQLite y migraciones.

Implementar configuración y rutas locales.

Crear una interfaz web mínima.

Añadir GET /api/health.

Añadir el CRUD básico de reuniones.

Añadir tests.

Crear un README con instrucciones.

Ejecutar tests y corregir errores.

Mostrar un resumen de los archivos creados.

Indicar el siguiente paso exacto.

No debe crear docenas de archivos vacíos sin implementación útil.

21. Prompt operativo para Codex
Utiliza esta sección como instrucción directa:

Construye este proyecto desde cero siguiendo esta especificación.

Empieza únicamente por la Fase 0 y la primera parte de la Fase 1:
- estructura;
- configuración;
- logging;
- SQLite;
- migraciones;
- FastAPI;
- interfaz web mínima;
- CRUD de reuniones;
- importación básica de archivos;
- cola de trabajos simple;
- tests.

Mantén el código modular y ejecutable.
No copies código ni diseño de otros productos.
No implementes todavía captura específica de Windows, macOS o Linux.
Crea interfaces limpias para las capas que llegarán después.
No dejes implementaciones ficticias que aparenten funcionar.
Usa errores explícitos para funcionalidades no disponibles.
Ejecuta los tests antes de finalizar.
Actualiza README.md con instalación y uso.
Al terminar, entrega:
1. resumen de arquitectura;
2. archivos creados;
3. comandos para ejecutar;
4. resultado de tests;
5. siguientes tareas recomendadas.
22. Principio final
La prioridad no es tener todas las funciones cuanto antes.

La prioridad es construir una base donde se puedan añadir sin rehacer el proyecto:

captura
transcripción
diarización
reconocimiento de hablantes
resumen
chat
calendario
detección de reuniones
GPU
sistemas operativos
empaquetado
Cada capacidad debe ser una capa intercambiable y comprobable.

