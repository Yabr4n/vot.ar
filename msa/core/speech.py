# -*- coding: utf-8 -*-
import os
import time

from hashlib import sha256
from threading import Thread

from msa.core.audioplayer import WavPlayer
from msa.settings import PATH_TTS
from msa.core.data.settings import JUEGO_DE_DATOS
from msa.voto.settings import VOLUMEN_GENERAL


_audio_player = None


class Locutor(Thread):

    def __init__(self):
        Thread.__init__(self)
        global _audio_player
        if _audio_player is None or not _audio_player.is_alive():
            _audio_player = WavPlayer()
            _audio_player.start()
            _audio_player.set_volume(VOLUMEN_GENERAL)
        self.reset()
        self.setDaemon(True)

    def run(self):
        while True:
            if self.mensaje and not _audio_player.pending_files():
                self._encolar(self.mensaje)
            if not self.repetir:
                self.mensaje = None
            time.sleep(0.1)

    def reset(self):
        self.mensaje = None
        self.repetir = False

    def decir(self, mensaje, repetir=False):
        """ Dice el mensaje recibido, si el mensaje es None, lo calla.

            Argumentos:
            mensaje -- Mensaje a decir
            repite -- Si es True, repite el mensaje (default False)
        """
        _audio_player.empty_queue()
        self.repetir = repetir
        if mensaje:
            if type(mensaje) is not list:
                mensaje = list(mensaje)
            if repetir:
                mensaje.append(WavPlayer.PAUSE_TOKEN)
            self.mensaje = mensaje

    def _encolar(self, mensaje):
        for m in mensaje:
            file_name = sha256(m.encode("ascii", "ignore")).hexdigest()
            _audio_player.queue_play(os.path.join(PATH_TTS, JUEGO_DE_DATOS,
                                                  file_name), m)

    def shutup(self):
        self.reset()
        _audio_player.empty_queue()
