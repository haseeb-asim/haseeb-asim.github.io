(function () {
  var canvas = document.querySelector("[data-field]");
  if (!canvas || !document.documentElement.classList.contains("motion")) return;
  if (!window.matchMedia("(min-width: 900px)").matches) return;
  var gl = canvas.getContext("webgl", { alpha: true, antialias: true, premultipliedAlpha: true });
  if (!gl) return;
  gl.getExtension("OES_standard_derivatives");

  function compile(type, src) {
    var shader = gl.createShader(type);
    gl.shaderSource(shader, src);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      canvas.remove();
      return null;
    }
    return shader;
  }

  var vs = compile(gl.VERTEX_SHADER, "attribute vec2 a;void main(){gl_Position=vec4(a,0.0,1.0);}");
  var fs = compile(gl.FRAGMENT_SHADER, [
    "#extension GL_OES_standard_derivatives : enable",
    "precision highp float;",
    "uniform vec2 uRes;",
    "uniform float uTime;",
    "uniform vec2 uMouse;",
    "uniform vec3 uColor;",
    "void main(){",
    "  vec2 uv=gl_FragCoord.xy/uRes;",
    "  vec2 aspect=vec2(uRes.x/max(uRes.y,1.0),1.0);",
    "  vec2 p=(uv-0.5)*aspect;",
    "  vec2 m=(uMouse-0.5)*aspect;",
    "  vec2 d=p-m;",
    "  float dist=length(d);",
    "  vec2 bend=d*(0.22/(dist+0.22));",
    "  vec2 q=p+bend*0.42+vec2(uTime*0.015, sin(uTime*0.2)*0.01);",
    "  float cells=34.0;",
    "  vec2 g=q*vec2(cells*aspect.x, cells);",
    "  vec2 f=fract(g)-0.5;",
    "  float r=length(f);",
    "  float aa=max(fwidth(r), 1.2/max(uRes.y,1.0));",
    "  float radius=0.055+0.05*(1.0-smoothstep(0.0,0.7,dist));",
    "  float dots=1.0-smoothstep(radius, radius+aa*1.6, r);",
    "  float ridge=abs(fract(q.y*14.0+sin(q.x*3.2+uTime*0.28)*0.28+bend.x*1.4)-0.5);",
    "  float lines=1.0-smoothstep(0.012, 0.012+aa*6.0, ridge);",
    "  float depth=0.28+0.72*smoothstep(0.95,0.05,dist);",
    "  float v=(dots*0.9+lines*0.28)*depth;",
    "  v*=smoothstep(0.78,0.18,length(p));",
    "  gl_FragColor=vec4(uColor*v, v);",
    "}"
  ].join("\n"));
  if (!vs || !fs) return;
  var program = gl.createProgram();
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) { canvas.remove(); return; }
  gl.useProgram(program);

  var buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  var loc = gl.getAttribLocation(program, "a");
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);

  var uRes = gl.getUniformLocation(program, "uRes");
  var uTime = gl.getUniformLocation(program, "uTime");
  var uMouse = gl.getUniformLocation(program, "uMouse");
  var uColor = gl.getUniformLocation(program, "uColor");
  var mouse = [0.68, 0.42];
  var target = [0.68, 0.42];
  var start = performance.now();
  var running = true;
  var visible = true;

  function accent() {
    var probe = document.createElement("span");
    probe.style.color = "var(--accent)";
    document.body.appendChild(probe);
    var c = getComputedStyle(probe).color;
    probe.remove();
    var parts = c.match(/[\d.]+/g) || [12, 68, 124];
    return [parts[0] / 255, parts[1] / 255, parts[2] / 255];
  }
  var color = accent();

  function resize() {
    var rect = canvas.getBoundingClientRect();
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = Math.max(1, Math.floor(rect.width * dpr));
    var h = Math.max(1, Math.floor(rect.height * dpr));
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
    }
    gl.viewport(0, 0, canvas.width, canvas.height);
  }
  resize();
  window.addEventListener("resize", resize);
  window.addEventListener("pointermove", function (event) {
    var rect = canvas.getBoundingClientRect();
    if (!rect.width) return;
    target[0] = (event.clientX - rect.left) / rect.width;
    target[1] = 1 - (event.clientY - rect.top) / rect.height;
  });
  var observer = new IntersectionObserver(function (entries) {
    visible = entries[0].isIntersecting;
    canvas.style.visibility = visible ? "visible" : "hidden";
  }, { threshold: 0.02 });
  observer.observe(canvas);
  document.addEventListener("visibilitychange", function () { running = !document.hidden; });
  var themeBtn = document.querySelector("[data-theme-toggle]");
  if (themeBtn) themeBtn.addEventListener("click", function () { color = accent(); });

  function frame(now) {
    requestAnimationFrame(frame);
    if (!running || !visible) return;
    mouse[0] += (target[0] - mouse[0]) * 0.06;
    mouse[1] += (target[1] - mouse[1]) * 0.06;
    gl.uniform2f(uRes, canvas.width, canvas.height);
    gl.uniform1f(uTime, (now - start) / 1000);
    gl.uniform2f(uMouse, mouse[0], mouse[1]);
    gl.uniform3f(uColor, color[0], color[1], color[2]);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }
  requestAnimationFrame(frame);
})();
